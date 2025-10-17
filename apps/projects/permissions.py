from rest_framework import permissions

from .choices import ProjectMemberRoleChoices


class IsOrgAdminOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.organization.owner:
            return True
        if obj.memberships.filter(
            user=request.user, role=ProjectMemberRoleChoices.MANAGER
        ).exists():
            return True
        return False
