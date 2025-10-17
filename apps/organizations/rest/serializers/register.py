from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from ...choices import OrganizationMemberRoleChoices
from ...models import Organization, OrganizationMember


User = get_user_model()


class OrganizationRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    organization_name = serializers.CharField(max_length=255)

    @transaction.atomic
    def create(self, validated_data):
        org_name = validated_data.pop("organization_name")
        user = User.objects.create_user(**validated_data)
        org = Organization.objects.create(name=org_name, created_by=user)
        OrganizationMember.objects.create(
            user=user,
            organization=org,
            role=OrganizationMemberRoleChoices.OWNER,
        )
        return user
