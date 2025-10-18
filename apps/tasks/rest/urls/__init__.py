from django.urls import path, include

urlpatterns = [
    path("status/", include("apps.tasks.rest.urls.task_status")),
]
