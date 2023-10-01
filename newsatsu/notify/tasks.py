from smtplib import SMTPException

from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.db.models import Case, When

from config import celery_app

from .api.serializers import NotificationSerializer
from .models import NotificationModel


def mail_send_func(notification):
    sender_email = settings.DEFAULT_FROM_EMAIL
    connection = get_connection()
    send_flag = False

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
    except ImportError:
        SendGridAPIClient = None
        Mail = None

    if (
        SendGridAPIClient
        and Mail
        and hasattr(settings, "ANYMAIL")
        and settings.ANYMAIL["SENDGRID_API_KEY"]
        and notification.template_id
    ):
        sg_mail = Mail(from_email=sender_email, to_emails=[notification.user.email])
        sg_mail.template_id = notification.template_id
        sg_mail.dynamic_template_data = {"notification": NotificationSerializer(notification).data}
        sg = SendGridAPIClient(settings.ANYMAIL["SENDGRID_API_KEY"])
        try:
            response = sg.send(sg_mail)
        except Exception as e:  # noqa
            raise e
        if response and response.status_code >= 200 and response.status_code < 300:
            send_flag = True

    else:
        try:
            send_mail(
                subject=notification.title,
                from_email=sender_email,
                message=notification.content,
                recipient_list=[notification.user.email],
                connection=connection,
            )
            send_flag = True
        except SMTPException as error:
            raise error

    if send_flag:
        notification.on_mail = True
        notification.save()


@celery_app.task(rate_limit="1/m")
def send_emails():
    """
    Send Email Notification
    """
    limit = settings.EMAIL_BATCH_SEND_LIMIT

    pending = NotificationModel.objects.filter(on_mail=False).order_by(
        Case(When(updated_at=None, then=0), default=1), "updated_at", "created_at"
    )

    if limit is not None:
        pending = pending[:limit]
    for notify in pending:
        mail_send_func(notify)
