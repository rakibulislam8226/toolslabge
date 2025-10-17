from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TrucTools API",
        default_version="v1",
        description="TrucTools API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@tructools.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# Define API version
API_V1 = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    # rest_framework
    path("api-auth/", include("rest_framework.urls")),
    # Swagger URLs
    path(
        f"{API_V1}/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # JWT Authentication URLs
    path(f"{API_V1}/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{API_V1}/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{API_V1}/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # organizations
    path(f"{API_V1}/organizations/", include("apps.organizations.rest.urls")),
    # projects
    path(f"{API_V1}/projects/", include("apps.projects.rest.urls")),
    # tasks
    # path(f"{API_V1}/tasks/", include("apps.tasks.rest.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]


urlpatterns += (
    re_path(
        r"^(?!api|media|static/).*", TemplateView.as_view(template_name="app.html")
    ),
)
