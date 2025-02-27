import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from newsatsu.utils.models import TimeStampModel


class UserTypeModel(models.TextChoices):
    UNION = _("unions"), "管理組合"
    COMPANY = _("companies"), "施工会社"


class User(AbstractUser):
    """
    Default custom user model for ニューサツ.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("会社名"), blank=True, max_length=255)
    area = models.CharField(_("地域"), max_length=20)
    user_type = models.CharField(max_length=20, choices=UserTypeModel.choices)

    # address
    post_code = models.CharField(_("郵便番号"), max_length=20)
    prefecture = models.CharField(_("都道府県"), max_length=100)
    city = models.CharField(_("市区町村"), max_length=50)
    house_number = models.CharField(_("番地"), max_length=20)
    building_name = models.CharField(_("建物名"), max_length=100, null=True, blank=True)

    # site url
    url = models.CharField(_("ホームページ"), max_length=255, null=True, blank=True)

    is_verify = models.BooleanField(_("メール認証確認"), default=False)

    is_allow = models.BooleanField(_("利用承認"), default=False)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return self == request.user

    @staticmethod
    def has_create_permission(request):
        return True


class UnionModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def year_choices():
        return tuple([(r, r) for r in range(1950, datetime.date.today().year + 1)])

    # 規模
    total_units = models.IntegerField(_("総戸数"))
    floor_number = models.IntegerField(_("階数"))
    building_number = models.IntegerField(_("棟数"))

    age = models.IntegerField(_("築年数"), choices=year_choices(), null=True, blank=True)

    # size
    site_area = models.FloatField(_("敷地面積"), null=True, blank=True)
    building_area = models.FloatField(_("建築面積"), null=True, blank=True)
    total_floor_area = models.FloatField(_("延床面積"), null=True, blank=True)

    # date time
    year_month_regex = RegexValidator(regex=r"^\d{4}-\d{2}$", message="Year-month must be in the format 'YYYY-MM'")
    estimated_construction_time = models.CharField(
        _("想定工事時期"), null=True, blank=True, max_length=7, validators=[year_month_regex]
    )

    def __str__(self) -> str:
        return self.user.name

    class Meta:
        verbose_name = "管理組合"
        verbose_name_plural = "管理組合"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True


class UnionConstructionHistoryModel(models.Model):
    union = models.ForeignKey(UnionModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self) -> str:
        return self.union.user.name

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return self.union.user == request.user

    def has_object_destroy_permission(self, request):
        return self.union.user == request.user

    @staticmethod
    def has_create_permission(request):
        return True


class CompanyModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 会社規模
    capital_stock = models.FloatField(_("資本金"))
    sales_amount = models.FloatField(_("売上高"))
    employee_number = models.IntegerField(_("社員数"))

    founded_year = models.DateField(_("設立年"))
    business_condition = models.BooleanField(_("直近3期赤字の有無"))

    # 経営事項審査
    architecture_rating_value = models.CharField(_("総合評定値(建築)"), null=True, blank=True)
    waterproof_rating_value = models.CharField(_("総合評定値(防水)"), null=True, blank=True)
    painting_rating_value = models.CharField(_("総合評定値(塗装)"), null=True, blank=True)

    def __str__(self) -> str:
        return self.user.name

    class Meta:
        verbose_name = "施工会社"
        verbose_name_plural = "施工会社"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True


class CompanyAchievementModel(TimeStampModel):
    class AchievementType(models.TextChoices):
        SUB = _("sub_contractor"), "下請"
        PRIME = _("prime_contractor"), "元請"

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(choices=AchievementType.choices, max_length=20)
    title = models.CharField(max_length=512)
    content = models.TextField()

    price = models.FloatField()

    counter = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "実績"
        verbose_name_plural = "実績"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_destroy_permission(self, request):
        return self.user == request.user

    @staticmethod
    def has_create_permission(request):
        return request.user.user_type == "companies"


def pr_file_upload_directory_path(instance, filename):
    return f"prs/{instance.user.username}/{filename}"


class CompanyOverviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pr_text = models.TextField(null=True, blank=True)
    pr_image = models.FileField(upload_to=pr_file_upload_directory_path, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return self.user == request.user

    @staticmethod
    def has_create_permission(request):
        return request.user.user_type == "companies"


def user_file_upload_directory_path(instance, filename):
    return f"users/{instance.user.username}/{filename}"


class UserFileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_file_upload_directory_path)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = "提出書類"
        verbose_name_plural = "提出書類"


def generate_token():
    return f'{datetime.datetime.now().strftime("%Y%m-%d%H-%M%S")}-{str(uuid.uuid4())}'


class TokenTypeModel(models.TextChoices):
    CREATE = _("create"), "user create"
    PASSWORD = _("password"), "reset password"


class UserTokenModel(TimeStampModel):
    type = models.CharField(choices=TokenTypeModel.choices, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(
        unique=True,
        max_length=255,
        default=generate_token,
    )

    def __str__(self) -> str:
        return self.user.username
