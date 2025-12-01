from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from ..serializers.verification import (
    EmailVerificationSerializer,
    ResendVerificationEmailSerializer,
)
from ...tasks import send_verification_email


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email(request):
    """
    Verify user's email address using verification token
    """
    serializer = EmailVerificationSerializer(data=request.data)

    if serializer.is_valid():
        token = serializer.validated_data["token"]
        user = serializer.verify_email(token)

        return Response(
            {
                "message": "Email verified successfully!",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"message": "Email verification failed.", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def resend_verification_email(request):
    """
    Resend verification email to user
    """
    serializer = ResendVerificationEmailSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data["email"]
        user = serializer.get_user(email)

        # Get base URL from request
        scheme = "https" if request.is_secure() else "http"
        base_url = f"{scheme}://{request.get_host()}"

        # Send verification email via Celery
        send_verification_email.delay(user.id, base_url)

        return Response(
            {
                "message": f"Verification email sent to {email}. Please check your inbox."
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"message": "Failed to send verification email.", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def check_verification_status(request, email):
    """
    Check if an email address is verified
    """
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user = User.objects.get(email=email)
        return Response(
            {"email": email, "is_verified": user.is_verified}, status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        return Response(
            {"message": "User not found with this email address."},
            status=status.HTTP_404_NOT_FOUND,
        )
