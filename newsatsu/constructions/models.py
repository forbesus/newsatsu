from django.db import models
from django.utils.translation import gettext_lazy as _

from newsatsu.users.models import Union


class Construction(models.Model):
    union = models.ForeignKey(Union, on_delete=models.SET_NULL, null=True, blank=True)
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

    def save(self, *args, **kwargs) -> None:
        if self.not_selected:
            self.first_engineer = False
            self.second_engineer = False
            self.on_site_agent = False
        self.save(*args, **kwargs)

    class Meta:
        verbose_name = "工事"
        verbose_name_plural = "工事"
