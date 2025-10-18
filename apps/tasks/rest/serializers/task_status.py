from rest_framework import serializers

from ...models import TaskStatus


class TaskStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = [
            "id",
            "name",
            "slug",
            "position",
            "is_default",
            "organization",
        ]
        read_only_fields = ["slug", "organization"]
