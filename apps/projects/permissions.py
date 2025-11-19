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


class IsProjectManager(permissions.BasePermission):
    """Only project managers can perform certain actions."""

    def has_permission(self, request, view):
        task_id = view.kwargs.get("task_id")
        if not task_id:
            return False
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return False

        user = request.user
        return ProjectMember.objects.filter(
            user=user,
            project=task.project,
            role=ProjectMemberRoleChoices.MANAGER,
        ).exists()


class IsProjectMemberForComments(permissions.BasePermission):
    """
    Only project members can view or create comments.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        task_id = view.kwargs.get("task_id")
        if not task_id:
            return False
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return False

        return ProjectMember.objects.filter(
            user=request.user, project=task.project
        ).exists()

    def has_object_permission(self, request, view, obj):
        return ProjectMember.objects.filter(
            user=request.user, project=obj.task.project
        ).exists()


class IsCommentAuthor(permissions.BasePermission):
    """Only comment authors can edit or delete their comments."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
