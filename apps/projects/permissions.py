from rest_framework import permissions

from apps.projects.choices import ProjectMemberRoleChoices
from apps.projects.models import ProjectMember


class IsProjectMemberOrManager(permissions.BasePermission):
    """Only project members can edit tasks.
    Managers/Admins can change status or reassign members.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not ProjectMember.objects.filter(user=user, project=obj.project).exists():
            return False

        if ProjectMember.objects.filter(
            user=user,
            project=obj.project,
            role__in=[
                ProjectMemberRoleChoices.MANAGER,
                ProjectMemberRoleChoices.CONTRIBUTOR,
            ],
        ).exists():
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.task_members.filter(member__user=user).exists()


class IsProjectMemberForComments(permissions.BasePermission):
    """
    Only project members can view or create comments.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Traverse to project via task
        project = obj.task.project

        # User must be a member of the project
        if not ProjectMember.objects.filter(user=user, project=project).exists():
            return False

        # Managers or contributors have full access
        if ProjectMember.objects.filter(
            user=user,
            project=project,
            role__in=[
                ProjectMemberRoleChoices.MANAGER,
                ProjectMemberRoleChoices.CONTRIBUTOR,
            ],
        ).exists():
            return True

        # Read-only methods are allowed for any project member
        if request.method in permissions.SAFE_METHODS:
            return True

        return False
