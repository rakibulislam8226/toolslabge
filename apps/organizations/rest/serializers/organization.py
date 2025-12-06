from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from ...choices import OrganizationMemberRoleChoices
from ...models import Organization, OrganizationMember
from apps.users.tasks import send_verification_email


User = get_user_model()


class OrganizationRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    photo = serializers.ImageField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True)
    organization_name = serializers.CharField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        org_name = validated_data.pop("organization_name")

        # Extract user data
        user_data = {
            "email": validated_data["email"],
            "password": validated_data["password"],
            "first_name": validated_data["first_name"],
            "last_name": validated_data["last_name"],
            "photo": validated_data.get("photo"),
        }

        user = User.objects.create_user(**user_data)
        org = Organization.objects.create(name=org_name, created_by=user)
        OrganizationMember.objects.create(
            user=user,
            organization=org,
            role=OrganizationMemberRoleChoices.OWNER,
        )

        # Send verification email with base URL from request
        if request:
            scheme = "https" if request.is_secure() else "http"
            base_url = f"{scheme}://{request.get_host()}"
            send_verification_email.delay(user.id, base_url)

        return user


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
