from rest_framework import permissions


class IsUserOwnerPermissions(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user
