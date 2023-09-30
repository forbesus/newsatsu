import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from newsatsu.notify.models import MailTypeModel, NotificationModel
from newsatsu.notify.tasks import mail_send_func
from newsatsu.users.models import CompanyModel, UnionModel, UserTokenModel

User = get_user_model()


def handle_company_register_event(sender, instance, created, **kwargs):
    try:
        if created:
            super_user = User.objects.filter(is_superuser=True)
            for super in super_user:
                template, _ = MailTypeModel.objects.get_or_create(name="user/create/")
                notification = NotificationModel(
                    user=super,
                    title="施工会社新規登録",
                    content=f"施工会社{instance.name}さんがプロフィールを登録しました。",
                    notify_type=ContentType.objects.get(CompanyModel).pk,
                    notify_id=instance.pk,
                    on_site=True,
                    template_id=template.template_id,
                )
                notification.save()
                mail_send_func(notification=notification)

            user = instance.user
            token = datetime.now().strftime("%Y%m-%d%H-%M%S-") + str(uuid.uuid4())
            user_token = UserTokenModel(user=user, token=token)
            user_token.save()

            template, _ = MailTypeModel.objects.get_or_create(name="user/register/")

            notification = NotificationModel(
                user=user,
                title="新規登録",
                content="プロフィールを登録しました。",
                notify_type=ContentType.objects.get(UserTokenModel).pk,
                notify_id=user_token.pk,
                on_site=True,
                template_id=template.template_id,
            )
            notification.save()
            mail_send_func(notification=notification)

    except Exception:
        pass


def handle_union_register_event(sender, instance, created, **kwargs):
    try:
        if created:
            super_user = User.objects.filter(is_superuser=True)
            for super in super_user:
                template, _ = MailTypeModel.objects.get_or_create(name="user/create/")
                notification = NotificationModel(
                    user=super,
                    title="管理組合新規登録",
                    content=f"管理組合{instance.name}さんがプロフィールを登録しました。",
                    notify_type=ContentType.objects.get(UnionModel).pk,
                    notify_id=instance.pk,
                    on_site=True,
                    template_id=template.template_id,
                )
                notification.save()
                mail_send_func(notification=notification)

            user = instance.user
            token = datetime.now().strftime("%Y%m-%d%H-%M%S-") + str(uuid.uuid4())
            user_token = UserTokenModel(user=user, token=token)
            user_token.save()

            template, _ = MailTypeModel.objects.get_or_create(name="user/register/")

            notification = NotificationModel(
                user=user,
                title="新規登録",
                content="プロフィールを登録しました。",
                notify_type=ContentType.objects.get(UserTokenModel).pk,
                notify_id=user_token.pk,
                on_site=True,
                template_id=template.template_id,
            )
            notification.save()
            mail_send_func(notification=notification)
    except Exception:
        pass
