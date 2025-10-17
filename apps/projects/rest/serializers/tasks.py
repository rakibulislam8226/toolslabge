from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskMember, TaskStatus
from apps.users.rest.serializers.slim_serializers import UserSlimSerializer

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    # Input
    project_id = serializers.PrimaryKeyRelatedField(
        source="project", queryset=Project.objects.none(), write_only=True
    )
    status_id = serializers.PrimaryKeyRelatedField(
        source="status",
        queryset=TaskStatus.objects.none(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )

    # Output
    project = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    assigned_members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "project_id",
            "project",
            "title",
            "description",
            "start_date",
            "due_date",
            "status_id",
            "status",
            "members",
            "assigned_members",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_by",
            "created_at",
            "updated_at",
            "project",
            "status",
            "assigned_members",
        ]

    def get_fields(self):
        fields = super().get_fields()
        user = self.context.get("request").user
        # Limit project choices to projects where user is a member
        fields["project_id"].queryset = Project.objects.filter(
            memberships__user=user
        ).distinct()
        # Limit status choices to user's organizations
        org_ids = user.organization_memberships.filter(is_active=True).values_list(
            "organization", flat=True
        )
        fields["status_id"].queryset = TaskStatus.objects.filter(
            organization__in=org_ids
        )
        return fields

    def get_project(self, obj):
        return {"id": obj.project.id, "name": obj.project.name}

    def get_status(self, obj):
        if not obj.status:
            return None
        return {
            "id": obj.status.id,
            "name": obj.status.name,
            "slug": getattr(obj.status, "slug", None),
        }

    def get_assigned_members(self, obj):
        task_members = obj.task_members.select_related("member__user")
        users = [tm.member.user for tm in task_members]
        return UserSlimSerializer(users, many=True).data

    def validate(self, data):
        user = self.context["request"].user
        project = data.get("project")

        if not project:
            raise serializers.ValidationError({"project_id": "Project is required."})

        # Ensure user is a project member
        if not ProjectMember.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError(
                {"project_id": "You must be a member of this project."}
            )

        # Validate dates
        start, due = data.get("start_date"), data.get("due_date")
        if start and due and start > due:
            raise serializers.ValidationError(
                {"due_date": "Due date must be after start date."}
            )

        # Validate members
        member_ids = self.initial_data.get("members", [])
        if member_ids:
            members_qs = ProjectMember.objects.filter(
                project=project, user__id__in=member_ids
            )
            if members_qs.count() != len(member_ids):
                invalid_ids = set(member_ids) - set(
                    members_qs.values_list("user__id", flat=True)
                )
                raise serializers.ValidationError(
                    {"members": f"Invalid members: {list(invalid_ids)}"}
                )
            self.context["validated_members"] = list(members_qs)
        else:
            self.context["validated_members"] = []

        # Validate status belongs to project organization
        status_obj = data.get("status")
        if status_obj and status_obj.organization_id != project.organization_id:
            raise serializers.ValidationError(
                {"status_id": "Status must belong to this project's organization."}
            )

        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        members = self.context.pop("validated_members", [])
        project = validated_data["project"]

        # Assign organization and creator
        validated_data["organization"] = project.organization
        validated_data["created_by"] = user

        # Determine status
        status = validated_data.pop("status", None)
        if not status:
            status = TaskStatus.objects.filter(
                organization=project.organization, is_default=True
            ).first()
            if not status:
                status = (
                    TaskStatus.objects.filter(organization=project.organization)
                    .order_by("position")
                    .first()
                )
        validated_data["status"] = status

        # Create task
        task = Task.objects.create(**validated_data)

        # Assign members
        TaskMember.objects.bulk_create(
            [TaskMember(task=task, member=m, assigned_by=user) for m in members]
        )

        return task
