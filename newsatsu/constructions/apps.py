from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class ContructionsConfig(AppConfig):
    name = "newsatsu.constructions"
    verbose_name = _("管理組合工事")
    verbose_name_plural = _("管理組合工事")

    def ready(self):
        try:
            from newsatsu.constructions.models import RequestCompanyModel
            from newsatsu.constructions.signals import handlers

            post_save.connect(handlers.request_company_event, sender=RequestCompanyModel)
        except ImportError:
            pass
