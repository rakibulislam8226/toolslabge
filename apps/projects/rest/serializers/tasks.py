from django.db import transaction
from rest_framework import serializers

from apps.projects.models import ProjectMember

from apps.tasks.models import Task, TaskMember

from apps.organizations.models import OrganizationMember
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    assigned_members = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "start_date",
            "due_date",
            "status",
            "members",  # input
            "assigned_members",  # output
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def get_assigned_members(self, obj):
        return [
            {
                "id": tm.member.user.id,
                "name": tm.member.user.get_full_name(),
                "email": tm.member.user.email,
                "role": tm.member.role,
            }
            for tm in obj.task_members.select_related("member__user")
        ]

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        project = data.get("project")
        member_ids = data.get("members", [])
        start_date = data.get("start_date")
        due_date = data.get("due_date")

        # Validate start_date and due_date
        if start_date and due_date and start_date > due_date:
            raise serializers.ValidationError(
                {"due_date": "Due date must be after start date."}
            )

        # Validate user is a project member
        if not ProjectMember.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError(
                "You must be this project's member to create tasks."
            )

        # Validate user is an organization member
        if not OrganizationMember.objects.filter(
            user=user, organization=project.organization
        ).exists():
            raise serializers.ValidationError(
                "You must be an organization member to assign tasks in this project."
            )

        # Fetch ProjectMembers from input user IDs
        members_qs = ProjectMember.objects.filter(
            project=project, user__id__in=member_ids
        )

        if members_qs.count() != len(member_ids):
            invalid_ids = set(member_ids) - set(
                members_qs.values_list("user__id", flat=True)
            )
            raise serializers.ValidationError(
                {
                    "members": f"These users are not part of this project: {list(invalid_ids)}"
                }
            )

        # Store validated members in context for use in create()
        self.context["validated_members"] = members_qs

        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        members = self.context["validated_members"]
        validated_data.pop("members", None)
        project = validated_data.get("project")
        organization = project.organization

        task = Task.objects.create(
            created_by=user,
            organization=organization,
            **validated_data,
        )

        for member in members:
            TaskMember.objects.create(task=task, member=member, assigned_by=user)

        return task
