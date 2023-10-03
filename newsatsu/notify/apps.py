from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save

# from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from newsatsu.utils.helpers.func_helpers import func_nothrow


class NotifyConfig(AppConfig):
    name = "newsatsu.notify"
    verbose_name = _("notify")
    verbose_name_plural = _("notifies")

    def ready(self) -> None:
        from newsatsu.notify.models import MailTypeModel, NotificationModel
        from newsatsu.notify.signals import handlers

        post_migrate.connect(MailTypeModel.create_default_types)

        post_save.connect(func_nothrow(handlers.handle_company_register_event), sender="users.CompanyModel")

        post_save.connect(func_nothrow(handlers.handle_union_register_event), sender="users.UnionModel")

        post_save.connect(func_nothrow(handlers.handle_send_mail_event), sender=NotificationModel)

        post_save.connect(func_nothrow(handlers.handle_register_user_token_event), sender="users.UserTokenModel")

        post_save.connect(
            func_nothrow(handlers.handle_request_company_event), sender="constructions.RequestCompanyModel"
        )
