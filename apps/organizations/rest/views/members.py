from rest_framework import generics

from ..serializers.members import OrganizationMembersListSerializer

from ...permissions import IsOrgOwnerAdminOrManager

from ...models import OrganizationMember


class OrganizationMembersListView(generics.ListAPIView):
    serializer_class = OrganizationMembersListSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        org_id = self.kwargs.get("org_id")
        return OrganizationMember.objects.filter(organization_id=org_id)
