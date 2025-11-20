from rest_framework import permissions

from apps.organizations.choices import OrganizationMemberRoleChoices


class IsOrgOwnerAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.organization_memberships.filter(
            user=request.user,
            role__in=[
                OrganizationMemberRoleChoices.OWNER,
                OrganizationMemberRoleChoices.ADMIN,
                OrganizationMemberRoleChoices.PROJECT_MANAGER,
                OrganizationMemberRoleChoices.MEMBER,
            ],
        ).exists():
            return True
        return False


class IsOrgOwnerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.organization_memberships.filter(
            user=request.user,
            role__in=[
                OrganizationMemberRoleChoices.OWNER,
                OrganizationMemberRoleChoices.ADMIN,
            ],
        ).exists():
            return True
        return False
