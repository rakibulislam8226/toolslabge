from rest_framework import serializers

from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from ...models import OrganizationMember


class OrganizationMembersListSerializer(serializers.ModelSerializer):
    user = UserSlimSerializer(read_only=True)

    class Meta:
        model = OrganizationMember
        fields = [
            "id",
            "user",
            "role",
            "is_active",
            "joined_at",
        ]
