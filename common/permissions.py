from rest_framework import permissions


class IsUserOwnerPermissions(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user


class IsCreatorOrHasModelPermission(permissions.BasePermission):
    """
    Object-level permission:
    - Allows creator to edit/delete their own object
    - Otherwise falls back to DjangoModelPermissions (handled globally)
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Creator can always edit or delete their own object
        if request.method in ["PUT", "PATCH", "DELETE"] and obj.created_by == user:
            return True

        return False
