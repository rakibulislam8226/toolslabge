from rest_framework import serializers

from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from apps.tasks.models import TaskComment, Task


class TaskCommentListSerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)

    class Meta:
        model = TaskComment
        fields = [
            "id",
            "content",
            "task",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "task",
            "author",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        task_id = self.context["view"].kwargs.get("task_id")
        task = Task.objects.get(id=task_id)

        return TaskComment.objects.create(
            created_by=user,
            author=user,
            task=task,
            **validated_data,
        )
