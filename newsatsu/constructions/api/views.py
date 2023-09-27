import json
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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
from newsatsu.users.models import CompanyModel, UnionModel

from .serializers import (
    BidSerializer,
    ConstructionSerializer,
    EvaluationSerializer,
    HearingSerializer,
    HireSerializer,
    RequestCompanySerializer,
    RequestQASerializer,
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

            construction = ConstructionModel(
                union=union,
                name=request.data.get("name"),
                content=request.data.get("content"),
                start_time=start_time,
                end_time=end_time,
                first_engineer=True if request.data.get("firstEngineer") == "true" else False,
                second_engineer=True if request.data.get("secondEngineer") == "true" else False,
                on_site_agent=True if request.data.get("onSiteAgent") == "true" else False,
                not_selected=True if request.data.get("notSelected") == "true" else False,
                question_request=request.data.get("questionRequest"),
                request_QA=request.data.get("requestQA"),
                end_QA=request.data.get("endQA"),
                quotation_request=request.data.get("quotationRequest"),
                company_request_number=request.data.get("requestNumber"),
                submit_document=request.data.get("submitDocument"),
                site_insurance=True if request.data.get("siteInsurance") == "true" else False,
                guarantee_insurance=True if request.data.get("guaranteeInsurance") == "true" else False,
            )
            construction.save()

            for key in request.data.keys():
                if key.startswith("file_"):
                    file = ConstructionFileModel(construction=construction, file=request.data[key])
                    file.save()

            return Response(data=ConstructionSerializer(construction).data, status=status.HTTP_201_CREATED)

        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request) -> Response:
        instance = self.get_object()
        data = request.data
        if "status" in data:
            update_status = request.data["status"]
            if update_status == "question":
                if instance.status == "request":
                    instance.status = update_status
                    instance.save()
            elif update_status == "answer":
                if instance.status == "question":
                    instance.status = update_status
                    instance.save()
            elif update_status == "bidding":
                if instance.status == "answer":
                    instance.status = update_status
                    instance.save()
            elif update_status == "hearing":
                if instance.status == "bidding":
                    instance.status = update_status
                    instance.save()
            elif update_status == "hiring":
                if instance.status == "hearing":
                    instance.status = update_status
                    instance.save()

            elif update_status == "evaluation":
                if instance.status == "hiring":
                    instance.status = update_status
                    instance.save()

        return Response(data=ConstructionSerializer(instance).data, status=status.HTTP_201_CREATED)


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


class RequestQAViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = RequestQASerializer
    queryset = RequestQAModel.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["construction"]

    def create(self, request: Request) -> Response:
        try:
            company = CompanyModel.objects.get(user=request.user)
            construction = ConstructionModel.objects.get(pk=request.data["construction"])
            request_question = RequestQAModel(
                question=request.data["question"], company=company, construction=construction
            )
            request_question.save()
            return Response(data=RequestQASerializer(request_question).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def csv_upload(self, request):
        try:
            answer_list = request.data["answers"]
            construction = ConstructionModel.objects.get(pk=request.data["construction"])
            for answer in answer_list:
                if answer["id"]:
                    request_qa = RequestQAModel.objects.get(pk=answer["id"], construction=construction)
                    request_qa.answer = answer["answer"]
                    request_qa.save()
            return Response(
                data=RequestQASerializer(RequestQAModel.objects.filter(construction=construction), many=True).data,
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)


class BidViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = BidSerializer
    queryset = BidModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["construction", "company__user__username"]

    def create(self, request: Request) -> Response:
        try:
            bid = BidModel(
                message=request.data["message"],
                amount=request.data["amount"],
                construction=ConstructionModel.objects.get(pk=request.data["construction"]),
                company=CompanyModel.objects.get(user=request.user),
            )
            bid.save()
            bid_file = BidFileModel(bid=bid, file=request.data["file"])
            bid_file.save()
            return Response(data=BidSerializer(bid).data, status=status.HTTP_201_CREATED)

        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)


class HearingViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = HearingSerializer
    queryset = HearingModel.objects.all()

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["company", "construction", "company__user__username", "status"]

    def create(self, request: Request) -> Response:
        hearing, created = HearingModel.objects.get_or_create(
            construction=ConstructionModel.objects.get(pk=request.data["construction"]),
            company=CompanyModel.objects.get(pk=request.data["company"]),
            start_time=request.data["start_time"],
            location=request.data["location"],
            contact_number=request.data["contact_number"],
        )
        hearing.save()
        return Response(data=HearingSerializer(hearing).data, status=status.HTTP_201_CREATED)


class HireViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = HireSerializer
    queryset = HireModel.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["construction", "company__user__username"]

    def create(self, request: Request) -> Response:
        hiring, created = HireModel.objects.get_or_create(
            construction=ConstructionModel.objects.get(pk=request.data["construction"]),
            company=CompanyModel.objects.get(pk=request.data["company"]),
        )
        hiring.save()
        return Response(data=HireSerializer(hiring).data, status=status.HTTP_201_CREATED)


class EvaluationViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = EvaluationSerializer

    queryset = EvaluationModel.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["construction", "company__user__username"]

    def create(self, request: Request) -> Response:
        evaluation, created = EvaluationModel.objects.get_or_create(
            construction=ConstructionModel.objects.get(pk=request.data["construction"]),
            company=CompanyModel.objects.get(pk=request.data["company"]),
        )
        if created:
            evaluation.quality = request.data["quality"]
            evaluation.correspondence = request.data["correspondence"]
            evaluation.safety = request.data["safety"]
            evaluation.period = request.data["period"]
            evaluation.maintenance = request.data["maintenance"]
            evaluation.comment = request.data["comment"]
            evaluation.save()
            return Response(data=EvaluationSerializer(evaluation).data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=EvaluationSerializer(evaluation).data, status=status.HTTP_201_CREATED)
