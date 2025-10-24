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
        project_id = self.kwargs.get("project_id")
        return (
            Task.objects.select_related("project", "project__organization", "status")
            .filter(project__id=project_id, project__memberships__user=user)
            .distinct()
        )


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsProjectMemberOrManager]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get("project_id")
        return Task.objects.select_related("project", "status", "organization").filter(
            project__id=project_id, project__memberships__user=user
        )
