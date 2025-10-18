from rest_framework import serializers

from apps.users.models import User
from apps.organizations.models import OrganizationMember


class UserOrganizationSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField(source="organization.id")
    organization_name = serializers.CharField(source="organization.name")
    organization_slug = serializers.CharField(source="organization.slug")
    role_display = serializers.CharField(source="get_role_display")

    class Meta:
        model = OrganizationMember
        fields = [
            "organization_id",
            "organization_name",
            "organization_slug",
            "role",
            "role_display",
            "is_active",
            "joined_at",
        ]


class MyInfoSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "photo",
            "username",
            "is_verified",
            "organizations",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "username",
            "is_verified",
            "organizations",
            "full_name",
            "created_at",
            "updated_at",
        ]

    def get_organizations(self, user):
        memberships = OrganizationMember.objects.filter(user=user, is_active=True)
        return UserOrganizationSerializer(memberships, many=True).data
