from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from ...models import Task, TaskMember
from ..serializers.tasks import MyTaskListCreateSerializer


class MyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = MyTaskListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Task.objects.select_related("project")
            .filter(task_members__member__user=self.request.user)
            .distinct()
        )
