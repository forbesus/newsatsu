import json
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from newsatsu.constructions.models import (
    BidModel,
    ConstructionModel,
    HearingModel,
    HireModel,
    RequestAnswerModel,
    RequestCompanyModel,
    RequestQuestionModel,
)
from newsatsu.users.models import CompanyModel, UnionModel

from .serializers import (
    BidSerializer,
    ConstructionSerializer,
    HearingSerializer,
    HireSerializer,
    RequestAnswerSerializer,
    RequestCompanySerializer,
    RequestQuestionSerializer,
)


class ConstructionViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = ConstructionSerializer
    queryset = ConstructionModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["union__user__username"]

    def create(self, request: Request) -> Response:
        try:
            union = UnionModel.objects.get(user=request.user)

            date_obj = datetime.strptime(request.data.get("startTime"), "%Y-%m")
            start_time = date_obj.strftime("%Y-%m-%d")

            date_obj = datetime.strptime(request.data.get("endTime"), "%Y-%m")
            end_time = date_obj.strftime("%Y-%m-%d")

            contruction = ConstructionModel(
                union=union,
                name=request.data.get("name"),
                content=request.data.get("content"),
                start_time=start_time,
                end_time=end_time,
                first_engineer=request.data.get("firstEngineer"),
                second_engineer=request.data.get("secondEngineer"),
                on_site_agent=request.data.get("onSiteAgent"),
                not_selected=request.data.get("notSelected"),
                question_request=request.data.get("questionRequest"),
                request_QA=request.data.get("requestQA"),
                end_QA=request.data.get("endQA"),
                quotation_request=request.data.get("quotationRequest"),
                company_request_number=request.data.get("requestNumber"),
                submit_document=request.data.get("submitDocument"),
                site_insurance=request.data.get("siteInsurance"),
                guarantee_insurance=request.data.get("guaranteeInsurance"),
            )
            contruction.save()
            return Response(data=ConstructionSerializer(contruction).data, status=status.HTTP_201_CREATED)

        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)


class RequestCompanyViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = RequestCompanySerializer
    queryset = RequestCompanyModel.objects.all()
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["company", "construction", "company__user__username"]

    def create(self, request: Request) -> Response:
        try:
            data = request.data
            construction = ConstructionModel.objects.get(union__user=request.user, pk=data.get("construction"))
            company = CompanyModel.objects.get(pk=data.get("company"))
            request_company, created = RequestCompanyModel.objects.get_or_create(
                construction=construction, company=company
            )
            return Response(data=RequestCompanySerializer(request_company).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)


class RequestQuestionViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = RequestQuestionSerializer
    queryset = RequestQuestionModel.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["construction"]

    def create(self, request: Request) -> Response:
        try:
            company = CompanyModel.objects.get(user=request.user)
            construction = ConstructionModel.objects.get(pk=request.data["construction"])
            request_question = RequestQuestionModel(
                content=request.data["content"], company=company, construction=construction
            )
            request_question.save()
            return Response(data=RequestQuestionSerializer(request_question).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)


class RequestAnswerViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = RequestAnswerSerializer
    queryset = RequestAnswerModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["construction"]


class BidViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = BidSerializer
    queryset = BidModel.objects.all()


class HearingViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = HearingSerializer
    queryset = HearingModel.objects.all()


class HireViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = HireSerializer
    queryset = HireModel.objects.all()
