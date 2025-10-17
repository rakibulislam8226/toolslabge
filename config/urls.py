from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Define API version
API_V1 = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT Authentication URLs
    path(f"{API_V1}/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{API_V1}/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{API_V1}/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # organizations
    path(f"{API_V1}/organizations/", include("apps.organizations.rest.urls")),
    # projects
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += (
    re_path(
        r"^(?!api|media|static/).*", TemplateView.as_view(template_name="app.html")
    ),
)
