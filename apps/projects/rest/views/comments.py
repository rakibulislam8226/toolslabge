from rest_framework import generics

from apps.tasks.models import TaskComment

from ...permissions import IsProjectMemberForComments
from ..serializers.comments import TaskCommentListSerializer


class TaskCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskCommentListSerializer
    permission_classes = [IsProjectMemberForComments]

    def get_queryset(self):
        user = self.request.user
        task_id = self.kwargs.get("task_id")

        return TaskComment.objects.filter(
            task_id=task_id, task__project__memberships__user=user
        ).select_related("author")
