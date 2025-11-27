from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskMember, TaskStatus, TaskDeadlineExtension
from apps.users.rest.serializers.slim_serializers import UserSlimSerializer

from ...tasks import send_task_assignment_email, send_member_remove_task_email

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
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
    my_project_role = serializers.SerializerMethodField(read_only=True)

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
            "priority",
            "estimated_hours",
            "status_id",
            "status",
            "members",
            "assigned_members",
            "my_project_role",
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
        return {"id": obj.project.id, "name": obj.project.name}

    def get_my_project_role(self, obj):
        user = self.context["request"].user
        membership = ProjectMember.objects.get(project=obj.project, user=user)
        return membership.role if membership else None

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

        if not ProjectMember.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError(
                {"project_id": "You must be a member of this project."}
            )

        start, due = data.get("start_date"), data.get("due_date")
        if start and due and start > due:
            raise serializers.ValidationError(
                {"due_date": "Due date must be after start date."}
            )

        # Validate members
        member_ids = self.initial_data.get("members", [])
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

        # Validate status belongs to project org
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

        validated_data.pop("members", None)
        project = validated_data.pop("project")
        status = validated_data.pop("status", None)

        # Set organization and creator
        validated_data["organization"] = project.organization
        validated_data["created_by"] = user

        # Determine status if not provided
        if not status:
            status = (
                TaskStatus.objects.filter(
                    organization=project.organization, is_default=True
                ).first()
                or TaskStatus.objects.filter(organization=project.organization)
                .order_by("position")
                .first()
            )
        validated_data["status"] = status

        task = Task.objects.create(project=project, **validated_data)

        TaskMember.objects.bulk_create(
            [TaskMember(task=task, member=m, created_by=user) for m in members]
        )
        # Send assignment emails
        for member in members:
            if user.id == member.user.id:
                continue  # don't send email to self
            task_url = self.context["request"].build_absolute_uri(
                f"/projects/{project.slug}/tasks/"
            )
            created_by = (
                user.first_name + " " + user.last_name
                if user.first_name and user.last_name
                else user.email
            )
            send_task_assignment_email.delay(
                member.user.first_name,
                member.user.email,
                task.title,
                task_url,
                created_by,
                project.name,
            )

        return task


class TaskDetailSerializer(serializers.ModelSerializer):
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

    # Read-only fields
    project = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    assigned_members = serializers.SerializerMethodField(read_only=True)
    deadline_extensions = serializers.SerializerMethodField(read_only=True)
    my_project_role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "slug",
            "description",
            "start_date",
            "due_date",
            "priority",
            "estimated_hours",
            "status_id",
            "status",
            "members",
            "assigned_members",
            "deadline_extensions",
            "my_project_role",
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

    def get_my_project_role(self, instance):
        user = self.context["request"].user
        membership = ProjectMember.objects.get(project=instance.project, user=user)
        return membership.role if membership else None

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user
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

    def get_deadline_extensions(self, obj):
        extensions = obj.deadline_extensions.all()
        return [
            {
                "id": ext.id,
                "previous_due_date": ext.previous_due_date,
                "new_due_date": ext.new_due_date,
                "reason": ext.reason,
                "created_at": ext.created_at,
                "created_by": ext.created_by.email if ext.created_by else None,
            }
            for ext in extensions
        ]

    def validate(self, data):
        user = self.context["request"].user
        instance = self.instance

        start, due = data.get("start_date"), data.get("due_date")
        if start and due and start > due:
            raise serializers.ValidationError(
                {"due_date": "Due date must be after start date."}
            )

        # Validate members (if given)
        member_ids = self.initial_data.get("members", [])
        if member_ids:
            members_qs = ProjectMember.objects.filter(
                project=instance.project, user__id__in=member_ids
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

        # Validate status belongs to same org
        status_obj = data.get("status")
        if status_obj and status_obj.organization_id != instance.organization_id:
            raise serializers.ValidationError(
                {"status_id": "Status must belong to this project's organization."}
            )

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context["request"].user
        members = self.context.pop("validated_members", [])

        # Handle member reassignment
        if "members" in self.initial_data:
            current_members = {tm.member_id: tm for tm in instance.task_members.all()}
            new_member_ids = {m.id for m in members}

            # Add new members
            to_add = new_member_ids - set(current_members.keys())
            TaskMember.objects.bulk_create(
                [
                    TaskMember(task=instance, member=m, created_by=user)
                    for m in members
                    if m.id in to_add
                ]
            )

            # Remove members not in new list
            to_remove = set(current_members.keys()) - new_member_ids
            if to_remove:
                instance.task_members.filter(member_id__in=to_remove).delete()

            # send to new members
            for member in members:
                if member.id in to_add:
                    if user.id == member.user.id:
                        continue  # don't send email to self
                    task_url = self.context["request"].build_absolute_uri(
                        f"/projects/{instance.project.slug}/tasks/"
                    )
                    created_by = (
                        user.first_name + " " + user.last_name
                        if user.first_name and user.last_name
                        else user.email
                    )
                    send_task_assignment_email.delay(
                        member.user.first_name,
                        member.user.email,
                        instance.title,
                        task_url,
                        created_by,
                        instance.project.name,
                    )

            # send to removed members
            for member_id in to_remove:
                if user.id == current_members[member_id].member.user.id:
                    continue  # don't send email to self
                member = current_members[member_id]
                task_url = self.context["request"].build_absolute_uri(
                    f"/projects/{instance.project.slug}/tasks/"
                )
                send_member_remove_task_email.delay(
                    member.member.user.first_name,
                    member.member.user.email,
                    instance.title,
                    instance.project.name,
                )

        # Handle status
        status = validated_data.get("status")
        if status and status.organization_id != instance.organization_id:
            raise serializers.ValidationError(
                {"status_id": "Status must belong to this project's organization."}
            )

        # Update allowed fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Track who made the change for signal
        instance._changed_by = user
        instance.save()

        return instance


class TaskDeadlineExtensionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDeadlineExtension
        fields = [
            "id",
            "task",
            "previous_due_date",
            "new_due_date",
            "reason",
            "created_at",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "previous_due_date",
            "created_at",
            "created_by",
        ]

    def validate_new_due_date(self, value):
        task = self.context["task"]
        if task.due_date and value <= task.due_date:
            raise serializers.ValidationError(
                "New due date must be after current due date."
            )
        return value

    def validate(self, data):
        task = self.context["task"]
        if not task:
            raise serializers.ValidationError("Invalid task.")
        if not task.due_date:
            raise serializers.ValidationError(
                "Task does not have a due date to extend."
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        task = self.context["task"]

        extension = TaskDeadlineExtension.objects.create(
            task=task,
            previous_due_date=task.due_date,
            new_due_date=validated_data["new_due_date"],
            reason=validated_data.get("reason", ""),
            created_by=user,
        )

        return extension

    def update(self, instance, validated_data):
        # Prevent updating previous_due_date and created_by
        validated_data.pop("previous_due_date", None)
        validated_data.pop("created_by", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
