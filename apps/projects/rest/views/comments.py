from rest_framework import generics

from apps.tasks.models import TaskComment

from ..serializers.comments import TaskCommentListSerializer
from ...permissions import IsProjectMemberForComments, IsCommentAuthor


class TaskCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskCommentListSerializer
    permission_classes = [IsProjectMemberForComments]

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return (
            TaskComment.objects.filter(task_id=task_id)
            .select_related("author")
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["task_id"] = self.kwargs.get("task_id")
        return context


class TaskCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskCommentListSerializer
    permission_classes = [IsCommentAuthor]
    queryset = TaskComment.objects.select_related("task", "author").order_by(
        "-created_at"
    )
