from rest_framework import serializers

from newsatsu.constructions.models import (
    BidModel,
    ConstructionModel,
    EvaluationModel,
    HearingModel,
    HireModel,
    RequestCompanyModel,
    RequestQAModel,
)
from newsatsu.users.api.serializers import CompanySerializer, UnionSerializer


class ConstructionSerializer(serializers.ModelSerializer):
    union = serializers.SerializerMethodField()

    def get_union(self, obj):
        return UnionSerializer(obj.union).data

    class Meta:
        model = ConstructionModel
        fields = "__all__"


class RequestCompanySerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    class Meta:
        model = RequestCompanyModel
        fields = "__all__"


class RequestQASerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    class Meta:
        model = RequestQAModel
        fields = "__all__"


class BidSerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    class Meta:
        model = BidModel
        fields = "__all__"


class HearingSerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    class Meta:
        model = HearingModel
        fields = "__all__"


class HireSerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    class Meta:
        model = HireModel
        fields = "__all__"


class EvaluationSerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    class Meta:
        model = EvaluationModel
        fields = "__all__"
