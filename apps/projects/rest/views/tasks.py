from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from ..serializers.tasks import TaskSerializer


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
