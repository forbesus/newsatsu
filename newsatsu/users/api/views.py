import json

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from newsatsu.users.models import CompanyAchievementModel, CompanyModel, UnionModel

from .serializers import CompanyAchievementSerializer, CompanySerializer, UnionSerializer, UserSerializer

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
            serializer = self.get_serializer(
                data={
                    "name": request.data["name"],
                    "email": request.data["email"],
                    "username": request.data["username"],
                    "password": request.data["password"],
                    "area": request.data["area"],
                    "user_type": request.data["user_type"],
                    "post_code": request.data["post_code"],
                    "prefecture": request.data["prefecture"],
                    "city": request.data["city"],
                    "house_number": request.data["house_number"],
                    "building_name": request.data["building_name"],
                    "url": request.data["url"],
                }
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            if request.data.get("user_type") == "companies":
                company = CompanyModel(
                    user=user,
                    capital_stock=request.data["capital_stock"],
                    sales_amount=request.data["sales_amount"],
                    employee_number=request.data["employee_number"],
                    founded_year=request.data["founded_year"],
                    business_condition=request.data["business_condition"],
                )
                company.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif request.data.get("user_type") == "unions":
                company = UnionModel(
                    user=user,
                    name=request.data["union_name"],
                    total_units=request.data["total_units"],
                    floor_number=request.data["floor_number"],
                    building_number=request.data["building_number"],
                    age=request.data["age"],
                    site_area=request.data["site_area"],
                    building_area=request.data["building_area"],
                    total_floor_area=request.data["total_floor_area"],
                    estimated_construction_time=request.data["estimated_construction_time"],
                )
                company.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanySerializer
    queryset = CompanyModel.objects.all()


class UnionViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = UnionSerializer
    queryset = UnionModel.objects.all()


class CompanyAchievementViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = CompanyAchievementSerializer
    queryset = CompanyAchievementModel.objects.all()

    def get_queryset(self, queryset, request):
        return queryset.filter(company__user=request.user)

    def create(
        self,
        request: Request,
    ) -> Response:
        try:
            data = request.data
            company = CompanyModel.objects.get(user=request.user)
            achieve = CompanyAchievementModel(
                company=company,
                type=data["type"],
                title=data["title"],
                content=data["content"],
                price=data["price"],
            )
            achieve.save()
            return Response(data=CompanyAchievementSerializer(achieve).data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(data=json.dumps(err.__dict__), status=status.HTTP_400_BAD_REQUEST)
