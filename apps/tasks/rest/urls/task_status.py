from django.urls import path

from ..views.task_status import (
    TaskStatusListCreateView,
    TaskStatusRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "",
        TaskStatusListCreateView.as_view(),
        name="task-status-list-create",
    ),
    path(
        "<int:pk>/",
        TaskStatusRetrieveUpdateDestroyView.as_view(),
        name="task-status-detail",
    ),
]
