from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..serializers.invitations import (
    SendInvitationSerializer,
    AcceptInvitationSerializer,
)

from ...permissions import IsOrgOwnerAdminOrManager

from ...choices import OrganizationMemberRoleChoices
from ...models import Organization


# FIXME:Permissions check exact organizationuser with org_id
class SendInvitationView(generics.CreateAPIView):
    serializer_class = SendInvitationSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_organization(self):
        org_id = self.kwargs.get("org_id")
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
            data=request.data, context={"organization": org, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        print("invitation token:", invitation.token)
        return Response(
            {
                "detail": f"Invitation sent to {invitation.email}.",
                "token": invitation.token,  # show for now (remove in prod)
            },
            status=status.HTTP_201_CREATED,
        )


class AcceptInvitationView(generics.CreateAPIView):
    serializer_class = AcceptInvitationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"detail": "Invitation accepted successfully. You can now log in."},
            status=status.HTTP_201_CREATED,
        )
