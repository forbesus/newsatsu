from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets

from newsatsu.notify.api.serializers import NewsSerializer, NotificationSerializer
from newsatsu.notify.models import NewsModel, NotificationModel


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = NotificationSerializer
    queryset = NotificationModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["on_site"]

    def get_queryset(self) -> QuerySet:
        queryset = NotificationModel.objects.filter(user=self.request.user).exclude(title="新規登録")

        return queryset


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = NewsSerializer
    queryset = NewsModel.objects.filter(display_status=True).order_by("created_at")
