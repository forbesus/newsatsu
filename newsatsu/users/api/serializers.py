from django.contrib.auth import get_user_model
from rest_framework import serializers

from newsatsu.users.models import CompanyAchievementModel, CompanyModel, UnionModel
from newsatsu.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["email", "username", "name", "user_type"]


class UnionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnionModel
        fields = "__all__"
        depth = 2


class CompanyAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAchievementModel
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = "__all__"
        depth = 2
