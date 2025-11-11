from django.urls import path

from ..views.tasks import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskExtendDeadlineListView,
    TaskExtendDeadlineDetailView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskRetrieveUpdateDestroyView.as_view(), name="task-detail"),
    path(
        "<int:task_id>/extend-deadline/",
        TaskExtendDeadlineListView.as_view(),
        name="task-extend-deadline",
    ),
    path(
        "<int:task_id>/extend-deadline/<int:pk>/",
        TaskExtendDeadlineDetailView.as_view(),
        name="task-extend-deadline-detail",
    ),
]
