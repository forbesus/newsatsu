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

    @staticmethod
    def has_create_permission(request):
        return True


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


class RequestQuestionModel(TimeStampModel):
    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True)
    content = models.TextField(_("質問"))

    def __str__(self) -> str:
        return self.content

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
        return False

    @staticmethod
    def has_create_permission(request):
        return True


class RequestAnswerModel(TimeStampModel):
    construction = models.ForeignKey(ConstructionModel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1024)
    answer = models.TextField()

    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name = "応答"
        verbose_name_plural = "応答"

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
        return False

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
        return False

    @staticmethod
    def has_create_permission(request):
        return True
