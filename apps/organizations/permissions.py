from rest_framework import permissions

from apps.organizations.choices import OrganizationMemberRoleChoices


class IsOrgOwnerAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(obj)
        if request.user.organization_memberships.filter(
            user=request.user, role=OrganizationMemberRoleChoices.OWNER
        ).exists():
            return True
        if request.user.organization_memberships.filter(
            user=request.user, role=OrganizationMemberRoleChoices.ADMIN
        ).exists():
            return True
        if request.user.organization_memberships.filter(
            user=request.user, role=OrganizationMemberRoleChoices.PROJECT_MANAGER
        ).exists():
            return True
        return False
