from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task, TaskDeadlineExtension

from ..serializers.tasks import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskDeadlineExtensionListSerializer,
)
from ...permissions import IsProjectMemberOrManager, IsProjectManager


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


class TaskExtendDeadlineListView(generics.ListCreateAPIView):
    serializer_class = TaskDeadlineExtensionListSerializer
    permission_classes = [IsProjectManager]

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return TaskDeadlineExtension.objects.filter(task_id=task_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        task_id = self.kwargs.get("task_id")
        try:
            context["task"] = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            context["task"] = None
        return context


class TaskExtendDeadlineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDeadlineExtensionListSerializer
    permission_classes = [IsProjectManager]

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return TaskDeadlineExtension.objects.filter(task_id=task_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        task_id = self.kwargs.get("task_id")
        try:
            context["task"] = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            context["task"] = None
        return context
