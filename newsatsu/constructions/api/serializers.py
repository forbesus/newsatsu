from rest_framework import serializers

from newsatsu.constructions.models import (
    BidFileModel,
    BidModel,
    ConstructionFileModel,
    ConstructionModel,
    EvaluationModel,
    HearingModel,
    HireModel,
    RequestCompanyModel,
    RequestQAModel,
)
from newsatsu.users.api.serializers import CompanySerializer, UnionSerializer


class ConstructionFileSerializer(serializers.ModelSerializer):
    file_info = serializers.SerializerMethodField()

    def get_file_info(self, obj):
        file = obj.file
        file_info = {
            "name": file.name,
            "url": file.url,
        }
        return file_info

    class Meta:
        model = ConstructionFileModel
        exclude = ["construction"]


class ConstructionSerializer(serializers.ModelSerializer):
    union = serializers.SerializerMethodField()

    def get_union(self, obj):
        return UnionSerializer(obj.union).data

    files = serializers.SerializerMethodField()

    def get_files(self, obj):
        return ConstructionFileSerializer(ConstructionFileModel.objects.filter(construction=obj), many=True).data

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


class BidFileSerializer(serializers.ModelSerializer):
    file_info = serializers.SerializerMethodField()

    def get_file_info(self, obj):
        file = obj.file
        file_info = {
            "name": file.name,
            "url": file.url,
        }
        return file_info

    class Meta:
        model = BidFileModel
        fields = ["file"]


class BidSerializer(serializers.ModelSerializer):
    construction = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    def get_construction(self, obj):
        return ConstructionSerializer(obj.construction).data

    def get_company(self, obj):
        return CompanySerializer(obj.company).data

    def get_files(self, obj):
        return BidFileSerializer(BidFileModel.objects.filter(bid=obj), many=True).data

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
