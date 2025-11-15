from rest_framework import generics

from common.permissions import IsUserOwnerPermissions

from ..serializers.tasks import MyTaskListCreateSerializer
from ...models import Task


class MyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = MyTaskListCreateSerializer
    permission_classes = [IsUserOwnerPermissions]

    def get_queryset(self):
        qs = (
            Task.objects.select_related("project")
            .filter(task_members__member__user=self.request.user)
            .distinct()
        )
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if status:
            qs = qs.filter(status__name=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs
