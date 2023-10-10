from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from newsatsu.constructions.api.serializers import (
    BidSerializer,
    HearingSerializer,
    HireSerializer,
    RequestCompanySerializer,
    RequestQASerializer,
)
from newsatsu.constructions.models import BidModel, HearingModel, HireModel, RequestCompanyModel, RequestQAModel
from newsatsu.notify.models import MailTypeModel, NewsModel, NotificationModel
from newsatsu.users.api.serializers import CompanySerializer, UnionSerializer, UserSerializer, UserTokenSerializer
from newsatsu.users.models import CompanyModel, UnionModel, User, UserTokenModel


class MailTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTypeModel
        fields = ["template_id", "path"]


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_template(self, obj):
        return MailTypeSerializer(obj.template).data

    notify = GenericRelatedField(
        {
            UserTokenModel: UserTokenSerializer(),
            User: UserSerializer(),
            UnionModel: UnionSerializer(),
            CompanyModel: CompanySerializer(),
            RequestCompanyModel: RequestCompanySerializer(),
            RequestQAModel: RequestQASerializer(),
            BidModel: BidSerializer(),
            HearingModel: HearingSerializer(),
            HireModel: HireSerializer(),
        }
    )

    class Meta:
        model = NotificationModel
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = ["news", "date"]
