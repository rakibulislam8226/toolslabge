from rest_framework import serializers

from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from apps.projects.models import Project, ProjectMember
from ...models import Task, TaskMember, TaskStatus


class MyTaskListCreateSerializer(serializers.ModelSerializer):
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
    project = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    assigned_members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "start_date",
            "due_date",
            "priority",
            "estimated_hours",
            "project_id",
            "project",
            "status_id",
            "status",
            "members",
            "assigned_members",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user
        fields["project_id"].queryset = Project.objects.filter(
            memberships__user=user
        ).distinct()
        org_ids = user.organization_memberships.filter(is_active=True).values_list(
            "organization", flat=True
        )
        fields["status_id"].queryset = TaskStatus.objects.filter(
            organization__in=org_ids
        )
        return fields

    def get_project(self, obj):
        return {
            "id": obj.project.id,
            "name": obj.project.name,
            "slug": obj.project.slug,
        }

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

    def validate(self, attrs):
        project = attrs.get("project")
        user = self.context["request"].user
        if not ProjectMember.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                "You are not a member of the specified project."
            )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        members_data = validated_data.pop("members", [])
        validated_data["created_by"] = user
        task = Task.objects.create(
            **validated_data,
            organization=user.organization_memberships.first().organization
        )

        for member_id in members_data:
            try:
                project_member = ProjectMember.objects.get(
                    id=member_id, project=task.project
                )
                TaskMember.objects.create(task=task, member=project_member)
            except ProjectMember.DoesNotExist:
                continue

        return task
