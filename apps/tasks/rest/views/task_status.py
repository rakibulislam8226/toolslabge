from rest_framework import generics

from apps.organizations.permissions import IsOrgOwnerAdmin

from ...models import TaskStatus
from ..serializers.task_status import TaskStatusListSerializer


class TaskStatusListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskStatusListSerializer
    permission_classes = [IsOrgOwnerAdmin]

    def get_queryset(self):
        user = self.request.user
        return TaskStatus.objects.filter(organization__memberships__user=user).order_by(
            "position"
        )

    def perform_create(self, serializer):
        org = self.request.user.organization_memberships.first().organization
        serializer.save(organization=org)


class TaskStatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskStatusListSerializer
    permission_classes = [IsOrgOwnerAdmin]

    def get_queryset(self):
        user = self.request.user
        return TaskStatus.objects.filter(organization__memberships__user=user)
