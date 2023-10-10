from django.contrib.auth import get_user_model
from rest_framework import serializers

from newsatsu.users.models import (
    CompanyAchievementModel,
    CompanyModel,
    CompanyOverviewModel,
    UnionConstructionHistoryModel,
    UnionModel,
)
from newsatsu.users.models import User as UserType
from newsatsu.users.models import UserFileModel, UserTokenModel

User = get_user_model()


class UserFileSerializer(serializers.ModelSerializer):
    file_info = serializers.SerializerMethodField()
    
    def get_file_info(self, obj):
        file = obj.file
        file_info = {
            'name': file.name,
            'url': file.url,
        }
        return file_info
    class Meta:
        model = UserFileModel
        fields = ["file", "file_info"]


class UserSerializer(serializers.ModelSerializer[UserType]):
    files = serializers.SerializerMethodField()

    def get_files(self, obj):
        return UserFileSerializer(UserFileModel.objects.filter(user=obj), many=True).data

    class Meta:
        model = User
        exclude = ["id", "password", "groups", "user_permissions", "is_staff", "first_name", "last_name"]


class UnionConstructionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnionConstructionHistoryModel
        fields = "__all__"


class UnionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_history(self, obj):
        return UnionConstructionHistorySerializer(
            UnionConstructionHistoryModel.objects.filter(union=obj), many=True
        ).data

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


class UserTokenSerializer(serializers.ModelSerializer):
    user = user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = UserTokenModel
        fields = ["user", "token"]
