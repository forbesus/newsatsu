from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets

from newsatsu.notify.api.serializers import NewsSerializer, NotificationSerializer
from newsatsu.notify.models import NewsModel, NotificationModel
from newsatsu.users.models import UserTokenModel


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = NotificationSerializer
    queryset = NotificationModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["on_site"]

    def get_queryset(self) -> QuerySet:
        queryset = NotificationModel.objects.filter(user=self.request.user).exclude(
            notify_type=ContentType.objects.get_for_model(UserTokenModel)
        )

        return queryset


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = NewsSerializer
    queryset = NewsModel.objects.filter(display_status=True).order_by("created_at")
