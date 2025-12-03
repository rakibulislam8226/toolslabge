from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that enforces email verification
    """

    def validate(self, attrs):
        """
        Validate user credentials and check if email is verified
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            if not user:
                raise serializers.ValidationError(
                    "No active account found with the given credentials"
                )

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            # Check if user's email is verified
            if not user.is_verified:
                raise serializers.ValidationError(
                    {
                        "email_not_verified": True,
                        "email": user.email,
                        "detail": "Please verify your email address before logging in. Check your inbox for a verification email.",
                    }
                )

            # Generate tokens for verified user
            refresh = RefreshToken.for_user(user)

            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
