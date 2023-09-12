# from django.contrib.contenttypes.models import ContentType


def request_company_event(sender, instance, **kwargs):
    if instance.status == "requesting":
        pass
        # notify_type = ContentType.objects.get_for_model(sender) # noqa
        # notify_id = instance.pk # noqa
        # title = "リクエスト通知"# noqa
        # content = f"通知があります。"# noqa
