from rest_framework import serializers

from newsatsu.notify.models import NotificationModel


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = "__all__"
