from rest_framework.permissions import BasePermission


class IsEmailVerified(BasePermission):
    """
    Custom permission to only allow access to verified users.
    """

    message = "You must verify your email address before accessing this resource."

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_verified
        )
