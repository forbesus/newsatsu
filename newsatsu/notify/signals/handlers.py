from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from newsatsu.notify.models import MailTypeModel, NotificationModel
from newsatsu.notify.tasks import mail_send_func
from newsatsu.users.models import CompanyModel, UnionModel, UserTokenModel

User = get_user_model()


def handle_company_register_event(sender, instance, created, **kwargs):
    try:
        if not created:
            super_user = User.objects.filter(is_superuser=True)
            for super in super_user:
                template, _ = MailTypeModel.objects.get_or_create(label="user/create/")
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
                mail_send_func(notification=notification)

            user = instance.user
            user_token = UserTokenModel(user=user)
            user_token.save()

            template, _ = MailTypeModel.objects.get_or_create(label="user/register/")

            notification = NotificationModel(
                user=user,
                title="新規登録",
                content="プロフィールを登録しました。",
                notify_type=ContentType.objects.get_for_model(UserTokenModel),
                notify_id=user_token.pk,
                on_site=True,
                template_id=template.template_id,
            )
            notification.save()
            mail_send_func(notification=notification)

    except Exception as err:
        print(err)
        pass


def handle_union_register_event(sender, instance, created, **kwargs):
    try:
        if not created:
            super_user = User.objects.filter(is_superuser=True)
            for super in super_user:
                template, _ = MailTypeModel.objects.get_or_create(label="user/create/")
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
                mail_send_func(notification=notification)

            user = instance.user
            user_token = UserTokenModel(user=user)
            user_token.save()

            template, _ = MailTypeModel.objects.get_or_create(label="user/register/")

            notification = NotificationModel(
                user=user,
                title="新規登録",
                content="プロフィールを登録しました。",
                notify_type=ContentType.objects.get_for_model(UserTokenModel),
                notify_id=user_token.pk,
                on_site=True,
                template_id=template.template_id,
            )
            notification.save()
            mail_send_func(notification=notification)
    except Exception as err:
        print(err)
        pass


def handle_send_mail_event(sender, instance, created, **kwargs):
    mail_send_func(instance)


def handle_register_user_token_event(sender, instance, created, **kwargs):
    template, _ = MailTypeModel.objects.get_or_create(label="user/register/")

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
