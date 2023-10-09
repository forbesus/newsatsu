from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save, pre_save

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

        pre_save.connect(func_nothrow(handlers.handle_allow_users_event), "users.User")

        post_save.connect(func_nothrow(handlers.handle_send_mail_event), sender=NotificationModel)

        post_save.connect(func_nothrow(handlers.handle_register_user_token_event), sender="users.UserTokenModel")

        post_save.connect(
            func_nothrow(handlers.handle_union_request_company_event), sender="constructions.RequestCompanyModel"
        )

        pre_save.connect(
            func_nothrow(handlers.handle_company_request_status_event), sender="constructions.RequestCompanyModel"
        )

        post_save.connect(func_nothrow(handlers.handle_company_question_event), sender="constructions.RequestQAModel")
        pre_save.connect(func_nothrow(handlers.handle_union_answer_event), sender="constructions.RequestQAModel")
        post_save.connect(func_nothrow(handlers.handle_company_bid_event), sender="constructions.BidModel")
        post_save.connect(
            func_nothrow(handlers.handle_union_request_hearing_event), sender="constructions.HearingModel"
        )
        pre_save.connect(
            func_nothrow(handlers.handle_company_hearing_status_event), sender="constructions.HearingModel"
        )
        post_save.connect(func_nothrow(handlers.handle_union_request_hiring_event), sender="constructions.HireModel")
