from django.urls import path
from ..views.comments import TaskCommentListCreateView

urlpatterns = [
    path(
        "",
        TaskCommentListCreateView.as_view(),
        name="task-comment-list-create",
    ),
]
