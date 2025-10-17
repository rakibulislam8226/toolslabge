from django.urls import path, include

urlpatterns = [
    path("", include("apps.projects.rest.urls.projects")),
]
