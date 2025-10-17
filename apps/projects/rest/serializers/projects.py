from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from apps.organizations.models import Organization

from ...choices import ProjectMemberRoleChoices
from ...models import Project, ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = ProjectMember
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "role",
            "created_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
        ]
        read_only_fields = ["status", "members"]

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )
        # Ensure project name is unique within the organization
        organization = (
            self.context["request"].user.organization_memberships.first().organization
        )
        if Project.objects.filter(
            organization=organization, name=data["name"]
        ).exists():
            raise serializers.ValidationError(
                {"name": "Project with this name already exists in the organization."}
            )

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        org_memberships = user.organization_memberships.filter(is_active=True)
        if not org_memberships.exists():
            raise serializers.ValidationError(
                "User does not belong to any active organization."
            )

        organization = org_memberships.first().organization

        validated_data.pop("organization", None)

        project = Project.objects.create(
            organization=organization,
            created_by=user,
            **validated_data,
        )

        # Auto-assign creator as project manager
        ProjectMember.objects.create(
            project=project,
            user=user,
            role=ProjectMemberRoleChoices.MANAGER,
            created_by=user,
        )

        return project
