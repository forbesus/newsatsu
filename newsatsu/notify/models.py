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
