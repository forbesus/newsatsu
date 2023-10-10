"""
There are event list for mail and notification

Event list start with handle_company_, are notifications and mails for Unions
and Event list start with handle_union_, are notifications and mails for Compannies
"""
import logging

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from newsatsu.constructions.models import BidModel, HearingModel, RequestCompanyModel, RequestQAModel
from newsatsu.notify.models import MailTypeModel, NotificationModel
from newsatsu.notify.tasks import mail_send_func
from newsatsu.users.models import CompanyModel, TokenTypeModel, UnionModel, UserTokenModel, UserTypeModel

User = get_user_model()


def handle_company_register_event(sender, instance, created, **kwargs):
    try:
        if created:
            super_user = User.objects.filter(is_superuser=True)
            for super in super_user:
                template, _ = MailTypeModel.objects.get_or_create(label="users/create/")
                notification = NotificationModel(
                    user=super,
                    title="施工会社新規登録",
                    content=f"施工会社{instance.user.name}さんがプロフィールを登録しました。",
                    notify_type=ContentType.objects.get_for_model(CompanyModel),
                    notify_id=instance.pk,
                    on_site=True,
                    template=template,
                )
                notification.save()

            user = instance.user
            user_token = UserTokenModel(user=user, type=TokenTypeModel.CREATE)
            user_token.save()

    except Exception as err:
        logging.error(err)
        pass


def handle_union_register_event(sender, instance, created, **kwargs):
    try:
        if created:
            super_user = User.objects.filter(is_superuser=True)
            for super in super_user:
                template, _ = MailTypeModel.objects.get_or_create(label="users/create/")
                notification = NotificationModel(
                    user=super,
                    title="管理組合新規登録",
                    content=f"管理組合{instance.user.name}さんがプロフィールを登録しました。",
                    notify_type=ContentType.objects.get_for_model(UnionModel),
                    notify_id=instance.pk,
                    on_site=True,
                    template=template,
                )
                notification.save()

            user = instance.user
            user_token = UserTokenModel(user=user, type=TokenTypeModel.CREATE)
            user_token.save()

    except Exception as err:
        print(err)
        pass


def handle_allow_users_event(sender, instance, update_fields, **kwargs):
    try:
        user = User.objects.get(pk=instance.pk)
        if not user.is_allow and instance.is_allow:
            if instance.user_type == UserTypeModel.UNION:
                template, _ = MailTypeModel.objects.get_or_create(label="allow/union/")
            elif instance.user_type == UserTypeModel.COMPANY:
                template, _ = MailTypeModel.objects.get_or_create(label="allow/company/")
            else:
                return False

            notification = NotificationModel(
                user=instance,
                title="ご登録情報が承認されました",
                content="ご登録情報が承認されました。どうぞ、サイトをご利用ください。",
                notify_type=ContentType.objects.get_for_model(sender),
                notify_id=instance.pk,
                on_site=True,
                template=template,
            )
            notification.save()

    except User.DoesNotExist:
        pass

    pass


def handle_send_mail_event(sender, instance, created, **kwargs):
    if created:
        mail_send_func(instance)


def handle_register_user_token_event(sender, instance, created, **kwargs):
    if created:
        if instance.type == TokenTypeModel.CREATE:
            if instance.user.user_type == UserTypeModel.UNION:
                template, _ = MailTypeModel.objects.get_or_create(label="register/union/")
            elif instance.user.user_type == UserTypeModel.COMPANY:
                template, _ = MailTypeModel.objects.get_or_create(label="register/company/")
            else:
                return False

            notification = NotificationModel(
                user=instance.user,
                title="新規登録",
                content="プロフィールを登録しました。",
                notify_type=ContentType.objects.get_for_model(UserTokenModel),
                notify_id=instance.pk,
                on_site=True,
                template=template,
            )
            notification.save()
        elif instance.type == TokenTypeModel.PASSWORD:
            template, _ = MailTypeModel.objects.get_or_create(label="users/reset-password/")

            notification = NotificationModel(
                user=instance.user,
                title="パスワード再設定",
                content="パスワード再設定",
                notify_type=ContentType.objects.get_for_model(UserTokenModel),
                notify_id=instance.pk,
                on_site=True,
                template=template,
            )
            notification.save()


def handle_union_request_company_event(sender, instance, created, **kwargs):
    if created:
        template, _ = MailTypeModel.objects.get_or_create(label="company/request/")

        notification = NotificationModel(
            user=instance.company.user,
            title="見積り依頼会社として選定されました",
            content=f"修繕工事{instance.construction.name}の見積もりをリクエストしています。",
            notify_type=ContentType.objects.get_for_model(RequestCompanyModel),
            notify_id=instance.pk,
            template=template,
        )
        notification.save()


def handle_union_answer_event(sender, instance, **kwargs):
    try:
        question_answer = RequestQAModel.objects.get(pk=instance.pk)
        if (question_answer.answer == "" or question_answer.answer is None) and (
            instance.answer != "" or instance.answer is not None
        ):
            template, _ = MailTypeModel.objects.get_or_create(label="company/answer/")

            notification = NotificationModel(
                user=instance.company.user,
                title="質疑の回答がありました",
                content=f"{instance.construction.union.user.name}管理組合様より、質疑の回答がありました。ご確認ください。",
                notify_type=ContentType.objects.get_for_model(RequestQAModel),
                notify_id=instance.pk,
                template=template,
            )
            notification.save()
    except Exception as err:
        logging.error(err)
        pass


def handle_union_request_hiring_event(sender, instance, created, **kwargs):
    if created:
        template, _ = MailTypeModel.objects.get_or_create(label="company/hiring/")

        notification = NotificationModel(
            user=instance.company.user,
            title="ヒアリング会の結果通知",
            content=f"{instance.construction.union.user.name}管理組合様より、ヒアリング会の結果が届きました。ご確認ください。",
            notify_type=ContentType.objects.get_for_model(RequestCompanyModel),
            notify_id=instance.pk,
            template=template,
        )
        notification.save()


def handle_union_request_hearing_event(sender, instance, created, **kwargs):
    if created:
        template, _ = MailTypeModel.objects.get_or_create(label="company/hearing/")

        notification = NotificationModel(
            user=instance.company.user,
            title="ヒアリング会への招待がありました",
            content=f"{instance.construction.union.user.name}管理組合様より、ヒアリング会の招待がありました。日程をご確認の上、ご対応お願い致します。",
            notify_type=ContentType.objects.get_for_model(HearingModel),
            notify_id=instance.pk,
            template=template,
        )
        notification.save()


def handle_company_request_status_event(sender, instance, **kwargs):
    try:
        request_company = RequestCompanyModel.objects.get(pk=instance.pk)
        if (
            request_company.status == RequestCompanyModel.RequestCompanyStatus.REQUESTING
            and instance.status
            and instance.status != RequestCompanyModel.RequestCompanyStatus.REQUESTING
        ):
            template, _ = MailTypeModel.objects.get_or_create(label="union/request-company/")

            notification = NotificationModel(
                user=instance.construction.union.user,
                title="見積り依頼会社から返信が届きました",
                content=f"修繕工事{instance.construction.name}の見積依頼をされた会社から返事が届きました。ご確認ください。",
                notify_type=ContentType.objects.get_for_model(RequestCompanyModel),
                notify_id=instance.pk,
                template=template,
            )
            notification.save()
    except Exception as err:
        logging.error(err)


def handle_company_question_event(sender, instance, created, **kwargs):
    if created:
        template, _ = MailTypeModel.objects.get_or_create(label="union/question-company/")

        notification = NotificationModel(
            user=instance.construction.union.user,
            title="施工会社様より返信が届きました",
            content=f"{instance.company.user.name}施行会社様より、ご質問が届きました。ご確認ください。",
            notify_type=ContentType.objects.get_for_model(RequestQAModel),
            notify_id=instance.pk,
            template=template,
        )
        notification.save()


def handle_company_bid_event(sender, instance, created, **kwargs):
    if created:
        template, _ = MailTypeModel.objects.get_or_create(label="union/quotation-company/")

        notification = NotificationModel(
            user=instance.construction.union.user,
            title="見積書の提出がされました",
            content=f"{instance.company.user.name}施行会社様より、見積書の提出がされました。ご確認ください。",
            notify_type=ContentType.objects.get_for_model(BidModel),
            notify_id=instance.pk,
            template=template,
        )
        notification.save()


def handle_company_hearing_status_event(sender, instance, **kwargs):
    try:
        hearing = HearingModel.objects.get(pk=instance.pk)
        if hearing.status == HearingModel.HearingStatus.REQUESTING and (
            instance.status == HearingModel.HearingStatus.ACCEPT
            or instance.status == HearingModel.HearingStatus.DECLINE
        ):
            template, _ = MailTypeModel.objects.get_or_create(label="union/hearing-company/")

            notification = NotificationModel(
                user=instance.construction.union.user,
                title="ヒアリング会への回答がありました",
                content=f"{instance.company.user.name}施行会社様より、ヒアイング会への回答がありました。ご確認ください。",
                notify_type=ContentType.objects.get_for_model(HearingModel),
                notify_id=instance.pk,
                template=template,
            )
            notification.save()
    except Exception as err:
        logging.error(err)
        pass
