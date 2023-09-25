from django.db import models
from django.utils.translation import gettext_lazy as _

from newsatsu.users.models import CompanyModel, UnionModel
from newsatsu.utils.models import TimeStampModel


class ConstructionModel(models.Model):
    class ConstructionStatus(models.TextChoices):
        REQUEST = _("request"), "見積依頼"
        QUESTION = _("question"), "質問"
        ANSWER = _("answer"), "応答"
        BID = _("bidding"), "入札"
        HEARING = _("hearing"), "ヒアリング会"
        HIRING = _("hiring"), "採用"
        EVALUATION = _("evaluation"), "入評価登録札"

    union = models.ForeignKey(UnionModel, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_("工事名"), max_length=255)
    content = models.TextField(_("工事内容"))
    start_time = models.DateField(_("予定工期 ー 開始"))
    end_time = models.DateField(_("予定工期 ー 終了"))

    # 現場代理人条件
    first_engineer = models.BooleanField(_("1級建築施工管理技士"), default=False)
    second_engineer = models.BooleanField(_("2級建築施工管理技士"), default=False)
    on_site_agent = models.BooleanField(_("現場代理人経験5年以上"), default=False)
    not_selected = models.BooleanField(_("指定しない"), default=False)

    # スケジュール
    question_request = models.DateField(_("見積もり依頼予定"))
    request_QA = models.DateField(_("質疑受付予定"))
    end_QA = models.DateField(_("質疑回答予定"))
    quotation_request = models.DateField(_("見積もり提出締切"))

    company_request_number = models.IntegerField(_("要請会社数"))

    submit_document = models.TextField(_("提出書類"))

    # 工事保険
    site_insurance = models.BooleanField(_("大規模修繕瑕疵保険加入"), null=True, blank=True)
    guarantee_insurance = models.BooleanField(_("履行保証保険加入"), null=True, blank=True)

    status = models.CharField(choices=ConstructionStatus.choices, default=ConstructionStatus.REQUEST, max_length=30)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if self.not_selected:
            self.first_engineer = False
            self.second_engineer = False
            self.on_site_agent = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "工事"
        verbose_name_plural = "工事"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return request.user == self.union.user

    @staticmethod
    def has_create_permission(request):
        return True


def construction_file_upload_directory_path(instance, filename):
    return f"constructions/{instance.construction.name}/{filename}"


class ConstructionFileModel(models.Model):
    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    file = models.FileField(upload_to=construction_file_upload_directory_path)

    def __str__(self) -> str:
        return self.construction.name


class RequestCompanyModel(models.Model):
    class RequestCompanyStatus(models.TextChoices):
        REQUESTING = _("requesting"), "見積依頼中"
        ACCEPT = _("accept"), "見積依頼"
        DECLINE = _("decline"), "見積辞退"
        REQUEST_UNSUCCESSFUL = _("unsuccessful"), "落選"

    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True)

    status = models.CharField(
        choices=RequestCompanyStatus.choices, default=RequestCompanyStatus.REQUESTING, max_length=20
    )

    def __str__(self):
        return f"{self.company.user.name}"

    class Meta:
        unique_together = ("company", "construction")
        verbose_name = "見積依頼会社"
        verbose_name_plural = "見積依頼会社"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return self.company.user == request.user

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.company.user

    @staticmethod
    def has_create_permission(request):
        return request.user


class RequestQAModel(TimeStampModel):
    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True)
    question = models.TextField(_("質問"))
    answer = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name = "質問"
        verbose_name_plural = "質問"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return self.construction.user == request.user

    @staticmethod
    def has_create_permission(request):
        return True


class BidModel(TimeStampModel):
    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(default=0)
    message = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("company", "construction")
        verbose_name = "入札会社"
        verbose_name_plural = "入札会社"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True


def bid_file_upload_directory_path(instance, filename):
    return f"bids/{instance.construction.name}/{instance.company.user.username}/{filename}"


class BidFileModel(TimeStampModel):
    bid = models.ForeignKey(BidModel, on_delete=models.CASCADE)
    file = models.FileField(upload_to=bid_file_upload_directory_path)


class HearingModel(TimeStampModel):
    class HearingStatus(models.TextChoices):
        REQUESTING = _("requesting"), "ヒアリング会への招待中"
        ACCEPT = _("accept"), "ヒアリング会承認"
        DECLINE = _("decline"), "ヒアリング会へ拒否"

    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(choices=HearingStatus.choices, default=HearingStatus.REQUESTING, max_length=20)

    location = models.CharField(_("住所"), max_length=30)
    start_time = models.DateTimeField(_("開始日"))
    contact_number = models.CharField(_("連絡番号"), max_length=30)

    def __str__(self) -> str:
        return self.construction.name

    class Meta:
        unique_together = ("company", "construction")
        verbose_name = "ヒアリング会"
        verbose_name_plural = "ヒアリング会"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.company.user

    @staticmethod
    def has_create_permission(request):
        return True


class HireModel(models.Model):
    class HireStatus(models.TextChoices):
        REQUESTING = _("requesting"), "採用中"
        ACCEPT = _("accept"), "採用承認"
        DECLINE = _("decline"), "採用辞退"
        WORK_UNSUCCESSFUL = _("unsuccessful"), "採用落選"
        FINISHED_WORK = _("finish"), "作業終了"
        EVALUATION = _("evaluation"), "入評価登録札"

    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(choices=HireStatus.choices, default=HireStatus.REQUESTING, max_length=20)

    def __str__(self) -> str:
        return self.construction.name

    class Meta:
        unique_together = ("company", "construction")
        verbose_name = "採用"
        verbose_name_plural = "採用"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True


class EvaluationModel(TimeStampModel):
    company = models.ForeignKey(CompanyModel, null=True, blank=True, on_delete=models.SET_NULL)
    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)

    quality = models.FloatField(_("品質"), null=True, blank=True)
    correspondence = models.FloatField(_("居住者対応"), null=True, blank=True)
    safety = models.FloatField(_("安全性"), null=True, blank=True)
    period = models.FloatField(_("工期"), null=True, blank=True)
    maintenance = models.FloatField(_("アフターメンテナンス"), null=True, blank=True)

    comment = models.TextField(_("コメント"), null=True, blank=True)

    def __str__(self) -> str:
        return self.company.user.username

    class Meta:
        unique_together = ("company", "construction")
        verbose_name = "工事の評価"
        verbose_name_plural = "工事の評価"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_update_permission(self, request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True
