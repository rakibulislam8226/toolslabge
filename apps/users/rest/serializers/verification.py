from rest_framework import serializers
from django.contrib.auth import get_user_model

from ...models import EmailVerificationToken


User = get_user_model()


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        try:
            verification_token = EmailVerificationToken.objects.get(token=value)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")

        if verification_token.is_used:
            raise serializers.ValidationError(
                "This verification token has already been used."
            )

        if verification_token.is_expired():
            raise serializers.ValidationError("This verification token has expired.")

        return value

    def verify_email(self, token):
        """Verify the email and mark token as used"""
        verification_token = EmailVerificationToken.objects.get(token=token)
        user = verification_token.user

        # Mark user as verified
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        # Mark token as used
        verification_token.is_used = True
        verification_token.save(update_fields=["is_used"])

        return user


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

        if user.is_verified:
            raise serializers.ValidationError("This email address is already verified.")

        return value

    def get_user(self, email):
        return User.objects.get(email=email)
