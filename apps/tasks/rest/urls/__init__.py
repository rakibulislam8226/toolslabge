from django.urls import path, include

urlpatterns = [
    path("", include("apps.tasks.rest.urls.tasks")),
    path("status/", include("apps.tasks.rest.urls.task_status")),
]
