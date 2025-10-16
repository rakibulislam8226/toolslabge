from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
]


urlpatterns += (
    re_path(
        r"^(?!api|media|static/).*", TemplateView.as_view(template_name="app.html")
    ),
)
