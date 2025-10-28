from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from ...models import Task, TaskMember
from ..serializers.tasks import MyTaskListCreateSerializer


class MyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = MyTaskListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (
            Task.objects.select_related("project")
            .filter(task_members__member__user=self.request.user)
            .distinct()
        )
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        print("Status filter:", status)

        if status:
            qs = qs.filter(status__name=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs
