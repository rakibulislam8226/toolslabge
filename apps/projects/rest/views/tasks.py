from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task

from ..serializers.tasks import TaskSerializer, TaskDetailSerializer
from ...permissions import IsProjectMemberOrManager


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Task.objects.select_related("project", "project__organization")
            .filter(project__memberships__user=user)
            .distinct()
        )


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsProjectMemberOrManager]
    queryset = Task.objects.select_related("project", "status", "organization")
