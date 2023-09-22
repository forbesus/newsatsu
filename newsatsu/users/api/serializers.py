from django.contrib.auth import get_user_model
from rest_framework import serializers

from newsatsu.users.models import CompanyAchievementModel, CompanyModel, CompanyOverviewModel, UnionModel
from newsatsu.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        exclude = ["id", "password", "groups", "user_permissions", "is_staff", "first_name", "last_name"]


class UnionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = UnionModel
        fields = "__all__"


class CompanyAchievementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = CompanyAchievementModel
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = CompanyModel
        fields = "__all__"


class CompanyOverviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = CompanyOverviewModel
        fields = "__all__"
