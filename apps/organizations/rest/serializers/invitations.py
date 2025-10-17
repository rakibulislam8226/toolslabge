import secrets

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from ...models import OrganizationInvitation, Organization, OrganizationMembership
from ...choices import OrganizationMembershipRoleChoices

User = get_user_model()


class SendInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=OrganizationMembershipRoleChoices.choices,
        default=OrganizationMembershipRoleChoices.MEMBER,
    )

    class Meta:
        model = OrganizationInvitation
        fields = ["email", "role"]

    def validate_email(self, value):
        org = self.context["organization"]
        if OrganizationInvitation.objects.filter(
            email=value, organization=org, accepted=False
        ).exists():
            raise serializers.ValidationError("This user has already been invited.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        org = self.context["organization"]
        invited_by = self.context["request"].user

        token = secrets.token_urlsafe(32)
        invitation = OrganizationInvitation.objects.create(
            organization=org,
            invited_by=invited_by,
            token=token,
            **validated_data,
        )

        # TODO: send email here
        return invitation


class AcceptInvitationSerializer(serializers.Serializer):
    token = serializers.CharField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            invitation = OrganizationInvitation.objects.get(
                token=data["token"], accepted=False
            )
        except OrganizationInvitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invitation token.")
        data["invitation"] = invitation
        return data

    @transaction.atomic
    def create(self, validated_data):
        invitation = validated_data["invitation"]
        email = invitation.email

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": validated_data["first_name"],
                "last_name": validated_data["last_name"],
            },
        )
        user.set_password(validated_data["password"])
        user.save()

        OrganizationMembership.objects.create(
            user=user,
            organization=invitation.organization,
            role=invitation.role,
        )

        invitation.accepted = True
        invitation.accepted_at = timezone.now()
        invitation.save()

        return user
