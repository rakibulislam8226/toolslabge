from rest_framework import permissions

from apps.tasks.models import Task


class IsTaskCreator(permissions.BasePermission):
    """Only project members can edit tasks.
    Managers/Admins can change status or reassign members.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.created_by == user
