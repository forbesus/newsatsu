from django.db import models
from django.utils.translation import gettext_lazy as _

from newsatsu.users.models import CompanyModel, UnionModel


class ConstructionModel(models.Model):
    class ConstructionStatus(models.TextChoices):
        REQUEST = _("見積依頼"), "request Quotation"
        QA = _("質疑応答"), "question and answer"
        BID = _("入札"), "bidding"
        HEARING = _("ヒアリング会"), "hearing party"
        HIRING = _("採用"), "hiring"
        EVALUATION = _("入評価登録札"), "evaluation"

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
    quotation_request = models.DateField(_("見積もり依頼予定"))
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
        self.save(*args, **kwargs)

    class Meta:
        verbose_name = "工事"
        verbose_name_plural = "工事"


class RequestCompanyModel(models.Model):
    class RequestCompanyStatus(models.TextChoices):
        REQUESTING = _("見積依頼中"), "requesting"
        REQUEST_ACCEPT = _("見積依頼"), "accept request"
        REQUEST_DECLINE = _("見積辞退"), "decline request"
        REQUEST_UNSUCCESSFUL = _("落選"), "unsuccessful"
        QA = _("質疑応答"), "question and answer"
        BID = _("入札"), "bidding"
        HEARING_REQUESTING = _("ヒアリング会への招待中"), "request hearing"
        HEARING_ACCEPT = _("ヒアリング会承認"), "accept hearing"
        HEARING_DECLINE = _("ヒアリング会へ拒否"), "accept decline"
        HIRING = _("採用中"), "hiring"
        HIRED = _("採用"), "hired"
        HIRING_UNSUCCESSFUL = _("採用落選"), "unsuccessful hire"
        FINISHED_WORK = _("作業終了"), "finished work"
        EVALUATION = _("入評価登録札"), "evaluation"

    construction = models.ForeignKey(ConstructionModel, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True, default=True)
    amount = models.FloatField(default=0)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(
        choices=RequestCompanyStatus.choices, default=RequestCompanyStatus.REQUESTING, max_length=20
    )

    def __str__(self):
        return f"{self.company.user.name}"

    class Meta:
        verbose_name = "見積依頼会社"
        verbose_name_plural = "見積依頼会社"
