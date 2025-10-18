from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from apps.organizations.models import Organization, OrganizationMember

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

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        project = self.context.get("project_id")
        organization = (
            user.organization_memberships.filter(is_active=True).first().organization
        )

        user_to_add = data.get("user")
        if not OrganizationMember.objects.filter(
            organization=organization,
            user=user_to_add,
            is_active=True,
        ).exists():
            raise serializers.ValidationError(
                {"user": "The user must be an active member of the organization."}
            )

        if ProjectMember.objects.filter(project=project, user=user_to_add).exists():
            raise serializers.ValidationError(
                {"user": "This user is already a member of the project."}
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        project = self.context.get("project_id")
        project = Project.objects.get(id=project)

        project_member = ProjectMember.objects.create(
            created_by=user,
            project=project,
            **validated_data,
        )
        return project_member


# FIXME: rethink project manager assignment. currently it take from organization member id. is it take this or user id?
class ProjectListSerializer(serializers.ModelSerializer):
    project_manager_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
            "project_manager_id",
        ]
        read_only_fields = ["status", "members"]

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )

        # Ensure user has active organization membership
        org_membership = user.organization_memberships.filter(is_active=True).first()
        if not org_membership:
            raise serializers.ValidationError(
                "User does not belong to any active organization."
            )

        organization = org_membership.organization
        data["organization"] = organization

        # Ensure project name is unique in the organization
        if Project.objects.filter(
            organization=organization, name=data["name"]
        ).exists():
            raise serializers.ValidationError(
                {"name": "Project with this name already exists in the organization."}
            )

        # Validate project_manager_id, if provided
        project_manager_id = self.initial_data.get("project_manager_id")
        if project_manager_id:
            try:
                org_member = OrganizationMember.objects.get(
                    id=project_manager_id, organization=organization
                )
                data["project_manager_user"] = org_member.user
            except OrganizationMember.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "project_manager_id": "Invalid ID or user is not part of the organization."
                    }
                )
        else:
            data["project_manager_user"] = user

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        organization = validated_data.pop("organization")
        project_manager_user = validated_data.pop("project_manager_user")
        validated_data.pop("project_manager_id", None)

        project = Project.objects.create(
            organization=organization,
            created_by=user,
            **validated_data,
        )

        ProjectMember.objects.create(
            project=project,
            user=project_manager_user,
            role=ProjectMemberRoleChoices.MANAGER,
            created_by=user,
        )

        return project


class ProjectDetailSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField(read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "start_date",
            "end_date",
            "status",
            "organization",
            "members",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "organization",
            "members",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        # fallback to existing values if partial update
        start_date = data.get("start_date", getattr(self.instance, "start_date", None))
        end_date = data.get("end_date", getattr(self.instance, "end_date", None))

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Only update allowed fields safely and trigger timestamp update.
        """
        allowed_fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
        ]

        for field, value in validated_data.items():
            if field in allowed_fields:
                setattr(instance, field, value)

        instance.updated_at = timezone.now()
        instance.save(update_fields=allowed_fields + ["updated_at"])

        return instance
