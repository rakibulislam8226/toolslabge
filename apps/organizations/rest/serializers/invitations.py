import secrets

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from ...choices import OrganizationMemberRoleChoices
from ...models import OrganizationInvitation, OrganizationMember
from ...tasks import send_invitation_email

User = get_user_model()


class SendInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=OrganizationMemberRoleChoices.choices,
        default=OrganizationMemberRoleChoices.MEMBER,
    )

    class Meta:
        model = OrganizationInvitation
        fields = ["email", "role"]

    def validate_email(self, value):
        org = self.context["organization"]
        invitations = OrganizationInvitation.objects.filter(
            email=value, organization=org
        )
        if invitations.filter(accepted=False).exists():
            raise serializers.ValidationError("This user has already been invited.")
        elif invitations.filter(accepted=True).exists():
            raise serializers.ValidationError(
                "This user is already a member of the organization."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        org = self.context["organization"]
        request = self.context["request"]

        created_by = request.user
        token = secrets.token_urlsafe(32)

        invitation = OrganizationInvitation.objects.create(
            organization=org,
            created_by=created_by,
            token=token,
            **validated_data,
        )

        # Build dynamic frontend URL using request
        base_url = request.build_absolute_uri("/")[:-1]
        accept_url = f"{base_url}/accept-invite/?token={token}"

        # Send email async
        send_invitation_email.delay(
            invitation.email,
            accept_url,
            org.name,
        )

        return invitation


class AcceptInvitationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        token = self.context["token"]

        try:
            invitation = OrganizationInvitation.objects.get(token=token, accepted=False)
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
                "is_verified": True,
            },
        )
        user.set_password(validated_data["password"])
        user.save()

        OrganizationMember.objects.create(
            user=user,
            organization=invitation.organization,
            role=invitation.role,
        )

        invitation.accepted = True
        invitation.accepted_at = timezone.now()
        invitation.save()

        return user
