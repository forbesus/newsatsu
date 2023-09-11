from django.db.models.query import QuerySet
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets

from newsatsu.notify.api.serializers import NotificationSerializer
from newsatsu.notify.models import NotificationModel


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = NotificationSerializer
    queryset = NotificationModel.objects.all()

    def get_queryset(self) -> QuerySet:
        queryset = NotificationModel.objects.filter(user=self.request.user, on_site=False)

        return queryset
