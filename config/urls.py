from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Alpha Apartments API",
        default_version="v1",
        description="Tenant Management API for Alpha Apartments",
        contact=openapi.Contact(email="bdas16001@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "api-doc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-ui",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("modules.users.urls")),
]

admin.site.site_header = "Alpha Apartments Admin"
admin.site.site_title = "Alpha Apartments Admin Portal"
admin.site.index_title = "Welcome to Alpha Apartments Admin Portal"
