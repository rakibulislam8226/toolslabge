from django.urls import path
from ..views.comments import TaskCommentListCreateView, TaskCommentDetailView

urlpatterns = [
    path(
        "",
        TaskCommentListCreateView.as_view(),
        name="task-comment-list-create",
    ),
    path(
        "<int:pk>/",
        TaskCommentDetailView.as_view(),
        name="task-comment-detail",
    ),
]
