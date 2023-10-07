from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from newsatsu.constructions.models import RequestCompanyModel
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
                    template_id=template.template_id,
                )
                notification.save()

            user = instance.user
            user_token = UserTokenModel(user=user, type=TokenTypeModel.CREATE)
            user_token.save()

    except Exception as err:
        print(err)
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
                    template_id=template.template_id,
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
                template_id=template.template_id,
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
                template_id=template.template_id,
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
                template_id=template.template_id,
            )
            notification.save()


def handle_request_company_event(sender, instance, created, **kwargs):
    if created:
        template, _ = MailTypeModel.objects.get_or_create(label="constructions/request-company/")

        notification = NotificationModel(
            user=instance.company.user,
            title="管理組合から大規模修繕工事の見積依頼が届いてます",
            content=f"修繕工事{instance.construction.name}の見積もりをリクエストしています。",
            notify_type=ContentType.objects.get_for_model(RequestCompanyModel),
            notify_id=instance.pk,
            template_id=template.template_id,
        )
        notification.save()
