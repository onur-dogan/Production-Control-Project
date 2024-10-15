from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="UAV-Rental-Project-with-Django",
        default_version="v1",
        description="UAV-Rental-Project-with-Django created by Onur Dogan",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aindres@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny),
)
