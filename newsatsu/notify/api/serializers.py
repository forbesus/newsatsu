from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from newsatsu.constructions.api.serializers import RequestCompanySerializer
from newsatsu.constructions.models import RequestCompanyModel
from newsatsu.notify.models import NotificationModel
from newsatsu.users.api.serializers import CompanySerializer, UnionSerializer, UserSerializer, UserTokenSerializer
from newsatsu.users.models import CompanyModel, UnionModel, User, UserTokenModel


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    notify = GenericRelatedField(
        {
            UserTokenModel: UserTokenSerializer(),
            User: UserSerializer(),
            UnionModel: UnionSerializer(),
            CompanyModel: CompanySerializer(),
            RequestCompanyModel: RequestCompanySerializer(),
        }
    )

    class Meta:
        model = NotificationModel
        fields = "__all__"
