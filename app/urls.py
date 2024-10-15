from django.contrib import admin
from django.urls import path, include
from .viewsets import (
    TeamViewSet,
    PartViewSet,
    UserViewSet,
    AircraftViewSet,
    PartStockViewSet,
    PartStockStatusViewSet,
    PartStockMobilityViewSet,
    AircraftProductionViewSet,
)
from .views.login import Login
from .views.signup import SignUp
from .views.parts import Parts, PartListView
from .views.aircrafts import Aircrafts, AircraftListView, AircraftProductionListView
from common.utils import logout
from common.swagger import schema_view
from rest_framework.routers import DefaultRouter

# Routers
router = DefaultRouter()
router.register(r"team", TeamViewSet)
router.register(r"user", UserViewSet)
router.register(r"part", PartViewSet)
router.register(r"partstock", PartStockViewSet)
router.register(r"partstockstatus", PartStockStatusViewSet)
router.register(r"partstockmobility", PartStockMobilityViewSet)
router.register(r"aircraft", AircraftViewSet)
router.register(r"aircraftproduction", AircraftProductionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # View Routers
    path("admin/", admin.site.urls),
    path("login/", Login.as_view(), name="login"),
    path("logout/", logout, name="logout"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("parts/", Parts.as_view(), name="parts"),
    path("partsData/", PartListView.as_view(), name="partsData"),
    path("aircrafts/", Aircrafts.as_view(), name="aircrafts"),
    path("aircraftsData/", AircraftListView.as_view(), name="aircraftsData"),
    path(
        "aircraftProductionsData/",
        AircraftProductionListView.as_view(),
        name="aircraftProductionsData",
    ),
    # Swagger Router
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
