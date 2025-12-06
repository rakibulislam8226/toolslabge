from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ...permissions import IsOrgOwnerAdmin
from rest_framework_simplejwt.tokens import RefreshToken

from apps.organizations.models import Organization
from apps.organizations.rest.serializers.organization import (
    OrganizationRegistrationSerializer,
    OrganizationDetailSerializer,
)


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


class OrganizationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrganizationDetailSerializer
    permission_classes = [IsOrgOwnerAdmin]

    def get_object(self):
        user = self.request.user
        membership = user.organization_memberships.filter(is_active=True).first()
        if not membership:
            return None
        return membership.organization
