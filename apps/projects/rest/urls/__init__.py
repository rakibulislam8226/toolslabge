from django.urls import path, include

urlpatterns = [
    path("", include("apps.projects.rest.urls.projects")),
    path("<int:project_id>/tasks/", include("apps.projects.rest.urls.tasks")),
    path(
        "<int:project_id>/tasks/<int:task_id>/comments/",
        include("apps.projects.rest.urls.comments"),
    ),
]
