from django.db.models import Max

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
        read_only_fields = [
            "id",
            "slug",
            "position",
            "is_default",
            "organization",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        org = user.organization_memberships.filter(is_active=True).first().organization

        max_position = (
            TaskStatus.objects.filter(organization=org).aggregate(Max("position"))[
                "position__max"
            ]
            or 0
        )
        next_position = max_position + 1

        # Remove 'organization' if present
        validated_data.pop("organization", None)

        return TaskStatus.objects.create(
            organization=org,
            position=next_position,
            is_default=False,
            **validated_data,
        )
