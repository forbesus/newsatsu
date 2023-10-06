from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from newsatsu.utils.models import TimeStampModel

User = get_user_model()


class NotificationModel(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    notify_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="+")
    notify_id = models.PositiveIntegerField()
    notify = GenericForeignKey("notify_type", "notify_id")
    on_mail = models.BooleanField(default=False)
    on_site = models.BooleanField(default=False)

    template_id = models.CharField(max_length=50)

    class Meta:
        verbose_name = "お知らせ"
        verbose_name_plural = "お知らせ"

    def __str__(self) -> str:
        return self.title

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.user

    @staticmethod
    def has_create_permission(request):
        return request.user


class MailTypeModel(models.Model):
    label = models.CharField(
        max_length=50,
        unique=True,
    )
    template_id = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "メールテンプレート"
        verbose_name_plural = "メールテンプレート"

    def __str__(self) -> str:
        return self.description

    class RepeatedCreation(Exception):
        pass

    @classmethod
    def create(cls, label, template_id="", description="", verbosity=1):
        try:
            mail_type = cls._default_manager.get(label=label)
            updated = False
            if mail_type.template_id != template_id:
                mail_type.template_id = template_id
                updated = True
            if mail_type.description != description:
                mail_type.description = description
                updated = True
            if updated:
                mail_type.save()
            if verbosity > 1:
                print("Updated %s MailType " % label)
        except cls.DoesNotExist:
            mail_type = cls(label=label, template_id=template_id)
            mail_type.save()

            if verbosity > 1:
                print("Created %s MailType" % label)

        return mail_type

    @classmethod
    def create_default_types(cls, **kwargs):
        cls.create(
            label="admin/create/user/",
            template_id="d-4f32172405384e7db1e2bcca4e371792",
            description="ユーザー登録通知",
        )
        cls.create(
            label="union/allow/",
            template_id="d-c737ebd8ee3849e4a7fa0c0d735bc72c",
            description="管理組合用・登録承認時",
        )
        cls.create(
            label="union/register/",
            template_id="d-4f32172405384e7db1e2bcca4e371792",
            description="管理組合用・登録時",
        )
        cls.create(
            label="union/request-company/",
            template_id="d-e4826a072fc84f8dbf4100e02cad8936",
            description="管理組合用・見積依頼",
        )
        cls.create(
            label="union/question-company/",
            template_id="d-f8649664407f4b258afc6622c79f3bb8",
            description="管理組合用・質問",
        )
        cls.create(
            label="union/quotation-company/",
            template_id="d-b26edcdf83ab47a7a76d51b5133fc1d9",
            description="管理組合用・見積",
        )
        cls.create(
            label="union/hearing-company/",
            template_id="d-0fe877786640496f953e1959b87d0c45",
            description="管理組合用・ヒアリング",
        )
        cls.create(
            label="union/other/",
            template_id="d-e9dcd56924b743d08955bb172c64a686",
            description="管理組合用・その他",
        )

        cls.create(
            label="company/other/",
            template_id="d-c150a1aa4db347e89568950448d1f5df",
            description="施工会社用・その他",
        )
        cls.create(
            label="company/hiring/",
            template_id="d-fdf052628e6e4adca6b33046316b99af",
            description="施工会社用・ヒアリング会後の結果",
        )
        cls.create(
            label="company/hearing/",
            template_id="d-02118881b3494f089c1d7679361eace9",
            description="施工会社用・ヒアリング会",
        )
        cls.create(
            label="company/answer/",
            template_id="d-c5406e11b074498fa6ca917e481293f8",
            description="施工会社用・回答",
        )
        cls.create(
            label="company/request/",
            template_id="d-2a926ae0584f4db193d708e265de6803",
            description="施工会社用・見積依頼",
        )
        cls.create(
            label="company/start-work/",
            template_id="d-559a2e1a25874aebabcaffdbf4f9228a",
            description="施工会社用 ・サイト利用開始",
        )
        cls.create(
            label="company/allow/",
            template_id="d-8b51c457079946e097df52c7f34c57be",
            description="施工会社用 ・登録承認後",
        )
        cls.create(
            label="company/register/",
            template_id="d-aac71fcab5b040c2b85879c2759f805e",
            description="施工会社用 ・登録時",
        )
        cls.create(
            label="users/reset-password/",
            template_id="d-b761ff894cbd46ce802ef11b1461dd6e",
            description="パスワードリセット",
        )


class NewsModel(TimeStampModel):
    news = models.TextField()

    date = models.DateField()

    display_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.news[:15] + "..."

    class Meta:
        verbose_name = "最近の状況"
        verbose_name_plural = "最近の状況"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    def has_object_write_permission(self, request):
        return False

    @staticmethod
    def has_create_permission(request):
        return False
