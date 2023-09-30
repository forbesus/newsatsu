from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from newsatsu.utils.models import TimeStampModel

User = get_user_model()


class NotificationModel(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    notify_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    notify_id = models.PositiveIntegerField()
    notify = GenericForeignKey("notify_type", "notify_id")
    on_mail = models.BooleanField(default=False)
    on_site = models.BooleanField(default=False)

    template_id = models.CharField(max_length=50)

    class Meta:
        verbose_name = "お知らせ"
        verbose_name_plural = "お知らせ"

    def __str__(self) -> str:
        return self.title

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return request.user

    def has_object_write_permission(self, request):
        return request.user

    @staticmethod
    def has_create_permission(request):
        return request.user


class MailTypeModel(models.Model):
    label = models.CharField(
        max_length=50,
        unique=True,
    )
    template_id = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.label

    class RepeatedCreation(Exception):
        pass

    @classmethod
    def create(cls, label, template_id="", description="", verbosity=1):
        try:
            mail_type = cls._default_manager.get(label=label)
            updated = False
            if mail_type.template_id != template_id:
                mail_type.template_id = template_id
                updated = True
            if mail_type.description != description:
                mail_type.description = description
                updated = True
            if updated:
                mail_type.save()
            if verbosity > 1:
                print("Updated %s MailType " % label)
        except cls.DoesNotExist:
            mail_type = cls(label=label, template_id=template_id)
            mail_type.save()

            if verbosity > 1:
                print("Created %s MailType" % label)

        return mail_type

    @classmethod
    def create_default_types(cls, **kwargs):
        cls.create(
            label="user/create/",
            template_id="d-4f32172405384e7db1e2bcca4e371792",
            description="user create mail for admin",
        )
        cls.create(
            label="user/register/",
            template_id="d-4f32172405384e7db1e2bcca4e371792",
            description="user create mail for users including unions and companies",
        )
