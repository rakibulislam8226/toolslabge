from apps.users.models import User
from apps.users.rest.serializers.profile import UserProfileDetailSerializer
from rest_framework import generics, permissions


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update the authenticated user's profile.
    """

    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
