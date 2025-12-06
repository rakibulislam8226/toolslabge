from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from apps.organizations.models import Organization, OrganizationMember
from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from apps.tasks.models import Task

from ...choices import ProjectMemberRoleChoices
from ...models import Project, ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    photo = serializers.ImageField(source="user.photo", read_only=True)

    class Meta:
        model = ProjectMember
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "role",
            "photo",
            "created_at",
        ]
        read_only_fields = ["id", "user_name", "user_email", "created_at"]

    def validate_role(self, value):
        """Validate that the role is one of the allowed choices."""
        from ...choices import ProjectMemberRoleChoices

        valid_roles = [choice[0] for choice in ProjectMemberRoleChoices.choices]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid role. Must be one of: {', '.join(valid_roles)}"
            )
        return value

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        project_slug = self.context.get("project_slug")
        # project_id = self.context.get("project_id")
        project = Project.objects.get(slug=project_slug)
        project_id = project.id

        # Only validate user membership during creation, not updates
        if not self.instance:  # This is a create operation
            organization = (
                user.organization_memberships.filter(is_active=True)
                .first()
                .organization
            )

            user_to_add = data.get("user")
            if (
                user_to_add
                and not OrganizationMember.objects.filter(
                    organization=organization,
                    user=user_to_add,
                    is_active=True,
                ).exists()
            ):
                raise serializers.ValidationError(
                    {"user": "The user must be an active member of the organization."}
                )

            if (
                user_to_add
                and ProjectMember.objects.filter(
                    project_id=project_id, user=user_to_add
                ).exists()
            ):
                raise serializers.ValidationError(
                    {"user": "This user is already a member of the project."}
                )
        else:
            # For updates, ensure we don't allow changing the user
            if "user" in data and data["user"] != self.instance.user:
                raise serializers.ValidationError(
                    {"user": "Cannot change the user of an existing project member."}
                )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        project_slug = self.context.get("project_slug")
        project = Project.objects.get(slug=project_slug)

        project_member = ProjectMember.objects.create(
            created_by=user,
            project=project,
            **validated_data,
        )
        return project_member

    def update(self, instance, validated_data):
        # Only allow updating the role field
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


class ProjectListSerializer(serializers.ModelSerializer):
    manager_id = serializers.IntegerField(write_only=True, required=False)
    my_project_role = serializers.SerializerMethodField(read_only=True)

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
            "manager_id",
            "my_project_role",
        ]
        read_only_fields = ["status", "slug"]

    def get_my_project_role(self, obj):
        """Get the role of the requesting user in this project."""
        request = self.context.get("request")
        user = request.user
        try:
            membership = obj.memberships.get(user=user)
            return membership.role
        except ProjectMember.DoesNotExist:
            return None

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

        # Validate manager_id, if provided
        manager_id = self.initial_data.get("manager_id")
        if manager_id:
            try:
                org_member = OrganizationMember.objects.get(
                    id=manager_id, organization=organization, is_active=True
                )
                data["manager_user"] = org_member.user
            except OrganizationMember.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "manager_id": "Invalid ID or user is not part of the organization."
                    }
                )
        else:
            # Default to current user as manager
            data["manager_user"] = user

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        organization = validated_data.pop("organization")
        manager_user = validated_data.pop("manager_user")
        validated_data.pop("manager_id", None)

        project = Project.objects.create(
            organization=organization,
            created_by=user,
            **validated_data,
        )

        # Create a ProjectMember entry for the manager with MANAGER role
        ProjectMember.objects.create(
            project=project,
            user=manager_user,
            role=ProjectMemberRoleChoices.MANAGER,
            created_by=user,
        )

        return project


class ProjectDetailSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField(read_only=True)
    manager = serializers.SerializerMethodField()
    members = ProjectMemberSerializer(many=True, read_only=True)
    my_project_role = serializers.SerializerMethodField(read_only=True)
    total_tasks = serializers.SerializerMethodField(read_only=True)
    total_members = serializers.SerializerMethodField(read_only=True)
    completed_tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "manager",
            "start_date",
            "end_date",
            "status",
            "organization",
            "members",
            "my_project_role",
            "total_tasks",
            "completed_tasks",
            "total_members",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "organization",
            "manager",
            "members",
            "created_at",
            "updated_at",
        ]

    def get_total_tasks(self, obj):
        return obj.tasks.count()

    def get_completed_tasks(self, obj):
        completed_status_names = ["Done", "Closed"]
        completed_tasks_count = Task.objects.filter(
            project=obj, status__name__in=completed_status_names
        ).count()
        return completed_tasks_count

    def get_total_members(self, obj):
        return obj.memberships.count()

    def get_my_project_role(self, obj):
        """Get the role of the requesting user in this project."""
        request = self.context.get("request")
        user = request.user
        try:
            membership = obj.memberships.get(user=user)
            return membership.role
        except ProjectMember.DoesNotExist:
            return None

    def get_manager(self, obj):
        """Get the project manager from ProjectMember with MANAGER role."""
        manager_member = obj.memberships.filter(
            role=ProjectMemberRoleChoices.MANAGER
        ).first()
        if manager_member:
            return UserSlimSerializer(manager_member.user).data
        return None

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
