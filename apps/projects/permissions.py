from rest_framework import generics, permissions
from apps.projects.models import ProjectMember
from apps.projects.choices import ProjectMemberRoleChoices


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
