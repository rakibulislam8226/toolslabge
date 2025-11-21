from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..serializers.invitations import (
    SendInvitationSerializer,
    AcceptInvitationSerializer,
)

from ...permissions import IsOrgOwnerAdminOrManager

from ...choices import OrganizationMemberRoleChoices
from ...models import Organization


class SendInvitationView(generics.CreateAPIView):
    serializer_class = SendInvitationSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        return Organization.objects.none()

    def get_organization(self):
        user = self.request.user
        org_id = (
            user.organization_memberships.filter(is_active=True).first().organization.id
        )
        return Organization.objects.get(id=org_id)

    def create(self, request, *args, **kwargs):
        org = self.get_organization()

        membership = request.user.organization_memberships.filter(
            organization=org, is_active=True
        ).first()
        if not membership or membership.role not in [
            OrganizationMemberRoleChoices.OWNER,
            OrganizationMemberRoleChoices.ADMIN,
        ]:
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            data=request.data,
            context={"organization": org, "request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Invitation sent successfully."},
            status=status.HTTP_201_CREATED,
        )


class AcceptInvitationView(generics.CreateAPIView):
    serializer_class = AcceptInvitationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        token = request.GET.get("token")

        if not token:
            return Response(
                {"detail": "Token is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data=request.data,
            context={"token": token},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Invitation accepted successfully. You can now log in."},
            status=status.HTTP_201_CREATED,
        )
