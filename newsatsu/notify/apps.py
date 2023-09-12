from django.apps import AppConfig

# from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class NotifyConfig(AppConfig):
    name = "newsatsu.notify"
    verbose_name = _("notify")
    verbose_name_plural = _("notifies")

    def ready(self) -> None:
        try:
            import newsatsu.notify.signals  # noqa: F401

        except ImportError:
            pass
