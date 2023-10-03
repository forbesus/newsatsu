from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from newsatsu.constructions.api.views import (
    BidViewSet,
    ConstructionViewSet,
    EvaluationViewSet,
    HearingViewSet,
    HireViewSet,
    RequestCompanyViewSet,
    RequestQAViewSet,
)
from newsatsu.notify.api.views import NotificationViewSet
from newsatsu.users.api.views import (
    CompanyAchievementViewSet,
    CompanyOverviewViewSet,
    CompanyViewSet,
    UnionConstructionHistoryViewSet,
    UnionViewSet,
    UserViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("unions", UnionViewSet)
router.register("achievements", CompanyAchievementViewSet)
router.register("constructions", ConstructionViewSet)
router.register("request-companies", RequestCompanyViewSet)
router.register("request-qa", RequestQAViewSet)
router.register("request-bidding", BidViewSet)
router.register("request-hearing", HearingViewSet)
router.register("request-hiring", HireViewSet)
router.register("request-evaluation", EvaluationViewSet)
router.register("notifies", NotificationViewSet)
router.register("overviews", CompanyOverviewViewSet)
router.register("union-histories", UnionConstructionHistoryViewSet)


app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
