from rest_framework import permissions

from apps.projects.choices import ProjectMemberRoleChoices
from apps.projects.models import ProjectMember
from apps.tasks.models import Task


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

    def has_permission(self, request, view):
        task_id = view.kwargs.get("task_id")
        if not task_id:
            return False
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return False

        # Check if user is a member of the task's project
        return ProjectMember.objects.filter(
            user=request.user, project=task.project
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Ensure user is a project member for object-level access
        return ProjectMember.objects.filter(
            user=request.user, project=obj.task.project
        ).exists()
