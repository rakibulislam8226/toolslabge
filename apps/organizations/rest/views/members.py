from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..serializers.members import OrganizationMembersListSerializer

from ...permissions import IsOrgOwnerAdminOrManager

from ...models import OrganizationMember


class OrganizationMembersListView(generics.ListAPIView):
    serializer_class = OrganizationMembersListSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        org_id = self.kwargs.get("org_id")
        return OrganizationMember.objects.filter(organization_id=org_id)


class MyOrganizationMembersListView(generics.ListAPIView):
    """
    List members from the logged-in user's organizations.
    This endpoint doesn't require org_id in the URL as it gets
    members from all organizations the user belongs to.
    """

    serializer_class = OrganizationMembersListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all organizations the current user is a member of
        user_orgs = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization_id", flat=True)

        # Return all members from those organizations
        return OrganizationMember.objects.filter(
            organization_id__in=user_orgs, is_active=True
        ).select_related("user", "organization")
