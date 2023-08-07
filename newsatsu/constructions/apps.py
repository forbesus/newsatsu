from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContructionsConfig(AppConfig):
    name = "newsatsu.constructions"
    verbose_name = _("管理組合工事")
    verbose_name_plural = _("管理組合工事")

    def ready(self):
        try:
            import newsatsu.constructions.signals  # noqa: F401
        except ImportError:
            pass
