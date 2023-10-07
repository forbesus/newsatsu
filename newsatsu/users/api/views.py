import json
from typing import Any

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from newsatsu.users.models import (
    CompanyAchievementModel,
    CompanyModel,
    CompanyOverviewModel,
    TokenTypeModel,
    UnionConstructionHistoryModel,
    UnionModel,
    UserFileModel,
    UserTokenModel,
)

from .serializers import (
    CompanyAchievementSerializer,
    CompanyOverviewSerializer,
    CompanySerializer,
    UnionConstructionHistorySerializer,
    UnionSerializer,
    UserSerializer,
    UserTokenSerializer,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    @action(detail=False, methods=["POST"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        try:
            user = User(
                name=request.data["name"],
                email=request.data["email"],
                username=request.data["username"],
                password=request.data["password"],
                area=request.data["area"],
                user_type=request.data["user_type"],
                post_code=request.data["post_code"],
                prefecture=request.data["prefecture"],
                city=request.data["city"],
                house_number=request.data["house_number"],
                building_name=request.data["building_name"],
                url=request.data.get("url", ""),
            )
            user.set_password(request.data["password"])
            user.save()

            for key in request.data.keys():
                if key.startswith("file_"):
                    user_file = UserFileModel(user=user, file=request.data[key])
                    user_file.save()

            if request.data.get("user_type") == "companies":
                company = CompanyModel(
                    user=user,
                    capital_stock=request.data["capital_stock"],
                    sales_amount=request.data["sales_amount"],
                    employee_number=request.data["employee_number"],
                    founded_year=request.data["founded_year"],
                    business_condition=bool(request.data["business_condition"]),
                )
                company.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            elif request.data.get("user_type") == "unions":
                company = UnionModel(
                    user=user,
                    total_units=request.data["total_units"],
                    floor_number=request.data["floor_number"],
                    building_number=request.data["building_number"],
                    age=request.data.get("age") if request.data.get("age") != "" else 0,
                    site_area=request.data.get("site_area") if request.data.get("site_area") != "" else 0,
                    building_area=request.data.get("building_area") if request.data.get("building_area") != "" else 0,
                    total_floor_area=request.data.get("total_floor_area")
                    if request.data.get("total_floor_area") != ""
                    else 0,
                    estimated_construction_time=request.data.get("estimated_construction_time"),
                )
                company.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            data = request.data
            user = request.user
            if "username" in data:
                user.username = data["username"]
            if "post_code" in data:
                user.post_code = data["post_code"]
            if "prefecture" in data:
                user.prefecture = data["prefecture"]
            if "city" in data:
                user.city = data["city"]
            if "house_number" in data:
                user.house_number = data["house_number"]
            if "building_name" in data:
                user.building_name = data["building_name"]
            if "url" in data:
                user.url = data["url"]
            user.save()
            if request.data.get("user_type") == "unions":
                union = UnionModel.objects.get(user=user)
                if "estimated_construction_time" in data:
                    union.estimated_construction_time = data["estimated_construction_time"]
                union.save()
                return Response(data=UnionSerializer(union).data, status=status.HTTP_206_PARTIAL_CONTENT)
            elif request.data.get("user_type") == "companies":
                if "area" in data:
                    user.area = data["area"]
                    user.save()
                company = CompanyModel.objects.get(user=user)
                if "capital_stock" in data:
                    company.capital_stock = data["capital_stock"]
                if "sales_amount" in data:
                    company.sales_amount = data["sales_amount"]
                if "employee_number" in data:
                    company.employee_number = data["employee_number"]
                if "founded_year" in data:
                    company.founded_year = data["founded_year"]
                if "business_condition" in data:
                    company.business_condition = True if data["business_condition"] == "1" else False
                company.save()
                return Response(data=CompanySerializer(company).data, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as err:
            print("err", err)
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def resend_verify(self, request: Request):
        try:
            email = request.data["email"]
            try:
                user = User.objects.get(email=email)
                user_token = UserTokenModel.objects.create(user=user, type=TokenTypeModel.CREATE)
                return Response(data=UserTokenSerializer(user_token).data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def verify_email(self, request: Request):
        try:
            token = request.data["token"]
            if token:
                user_token = UserTokenModel.objects.get(token=token, type=TokenTypeModel.CREATE)
                user = user_token.user
                user.is_verify = True
                user.save()
                return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)
        except UserTokenModel.DoesNotExist:
            return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def forgot_password(self, request: Request):
        try:
            email = request.data["email"]
            try:
                user = User.objects.get(email=email)
                user_token = UserTokenModel.objects.create(user=user, type=TokenTypeModel.PASSWORD)
                return Response(data=UserTokenSerializer(user_token).data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def reset_password(self, request: Request):
        try:
            token = request.data["token"]
            password = request.data["password"]
            if token and password:
                user_token = UserTokenModel.objects.get(token=token, type=TokenTypeModel.PASSWORD)
                user = user_token.user
                user.set_password(password)
                user.save()
                return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)
        except UserTokenModel.DoesNotExist:
            return Response(data="登録されていません。もう一度登録してください", status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanySerializer
    queryset = CompanyModel.objects.all()

    filter_backends = [DjangoFilterBackend]

    filterset_fields = {
        "user__name": ["exact", "in"],
        "user__area": ["exact"],
        "capital_stock": ["gte", "lte"],
        "sales_amount": ["gte", "lte"],
        "founded_year": ["gte", "lte"],
    }

    @action(detail=False, methods=["POST"])
    def get_profile(self, request):
        try:
            company = CompanyModel.objects.get(user=request.user)
            return Response(status=status.HTTP_200_OK, data=CompanySerializer(company).data)
        except CompanyModel.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="company is not exist")


class UnionViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = UnionSerializer
    queryset = UnionModel.objects.all()

    @action(detail=False, methods=["POST"])
    def get_profile(self, request):
        try:
            union = UnionModel.objects.get(user=request.user)
            return Response(status=status.HTTP_200_OK, data=UnionSerializer(union).data)
        except UnionModel.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="company is not exist")


class UnionConstructionHistoryViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = UnionConstructionHistorySerializer
    queryset = UnionConstructionHistoryModel.objects.all()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            title = request.data["title"]
            content = request.data["content"]
            union = UnionModel.objects.get(user=request.user)
            history = UnionConstructionHistoryModel(union=union, title=title, content=content)
            history.save()
            return Response(data=UnionConstructionHistorySerializer(history).data, status=status.HTTP_201_CREATED)
        except UnionModel.DoesNotExist:
            return Response(data="union is not exist", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        instance = self.get_object()
        if "title" in data and len(data["title"]) != 0:
            instance.title = data["title"]
        if "content" in data and len(data["content"]) != 0:
            instance.content = data["content"]
        instance.save()

        return Response(data=UnionConstructionHistorySerializer(instance).data, status=status.HTTP_206_PARTIAL_CONTENT)


class CompanyAchievementViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanyAchievementSerializer
    queryset = CompanyAchievementModel.objects.all()

    def create(
        self,
        request: Request,
    ) -> Response:
        try:
            data = request.data
            achieve = CompanyAchievementModel(
                user=request.user,
                type=data["type"],
                title=data["title"],
                content=data["content"],
                counter=data["counter"],
                price=data["price"],
            )
            achieve.save()
            return Response(data=CompanyAchievementSerializer(achieve).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def get_achieve(self, request):
        achieves = CompanyAchievementModel.objects.filter(user=request.user)
        return Response(data=CompanyAchievementSerializer(achieves, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_achieve_for_union(self, request):
        try:
            company_id = request.query_params.get("companyId")
            user = CompanyModel.objects.get(pk=company_id).user
            achieves = CompanyAchievementModel.objects.filter(user=user)
            return Response(data=CompanyAchievementSerializer(achieves, many=True).data, status=status.HTTP_200_OK)
        except CompanyModel.DoesNotExist:
            return Response(data="company is not exist", status=status.HTTP_400_BAD_REQUEST)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)


class CompanyOverviewViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanyOverviewSerializer
    queryset = CompanyOverviewModel.objects.all()

    def create(
        self,
        request: Request,
    ) -> Response:
        try:
            data = request.data
            overview = CompanyOverviewModel(
                user=request.user,
                pr_text=data["pr_text"],
            )
            overview.save()
            return Response(data=CompanyOverviewSerializer(overview).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def get_overview(self, request):
        overview, _ = CompanyOverviewModel.objects.get_or_create(user=request.user)
        return Response(data=CompanyOverviewSerializer(overview).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_overview_for_union(self, request):
        try:
            company_id = request.query_params.get("companyId")
            user = CompanyModel.objects.get(pk=company_id).user
            overview, _ = CompanyOverviewModel.objects.get_or_create(user=user)
            return Response(data=CompanyOverviewSerializer(overview).data, status=status.HTTP_200_OK)
        except CompanyModel.DoesNotExist:
            return Response(data="company is not exist", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            data = request.data
            user = request.user
            overview = CompanyOverviewModel.objects.get(user=user)
            overview.pr_text = data["pr_text"]
            overview.pr_image = data["pr_image"]
            overview.save()

            return Response(data=CompanyOverviewSerializer(overview).data, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)
