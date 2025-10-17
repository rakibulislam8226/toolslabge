from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers.register import OrganizationOwnerRegistrationSerializer


class RegisterOrganizationOwnerView(generics.CreateAPIView):
    serializer_class = OrganizationOwnerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"detail": "Organization and owner account created successfully."},
            status=status.HTTP_201_CREATED,
        )
