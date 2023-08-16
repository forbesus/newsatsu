from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from newsatsu.users.models import CompanyAchievementModel, CompanyModel, UnionModel

from .serializers import CompanyAchievementSerializer, CompanySerializer, UnionSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CompanyViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanySerializer
    queryset = CompanyModel.objects.all()


class UnionViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = UnionSerializer
    queryset = UnionModel.objects.all()


class CompanyAchievementViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanyAchievementSerializer
    queryset = CompanyAchievementModel.objects.all()
