from rest_framework import serializers

from newsatsu.constructions.models import (
    BidModel,
    ConstructionModel,
    HearingModel,
    HireModel,
    RequestAnswerModel,
    RequestCompanyModel,
    RequestQuestionModel,
)


class ConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionModel
        fields = "__all__"


class RequestCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCompanyModel
        fields = "__all__"
        depth = 2


class RequestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQuestionModel
        fields = "__all__"
        depth = 2


class RequestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestAnswerModel
        fields = "__all__"


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidModel
        fields = "__all__"


class HearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HearingModel
        fields = "__all__"


class HireSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireModel
        fields = "__all__"
