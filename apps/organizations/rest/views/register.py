from rest_framework import generics, permissions, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.register import OrganizationRegistrationSerializer


class RegisterOrganizationView(generics.CreateAPIView):
    serializer_class = OrganizationRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "detail": "Organization and owner account created successfully.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
