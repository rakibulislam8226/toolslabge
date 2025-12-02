import random
from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from rest_framework import generics, status, permissions
from rest_framework.exceptions import NotFound

from apps.users.models import User
from ..serializers.password_reset import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
    PasswordResetSerializer,
    UpdatePasswordSerializer,
)
from ...models import Otp, PasswordResetToken
from ...tasks import send_forgot_password_otp_email


class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    # permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password_reset_token = serializer.validated_data["password_reset_token"]
        new_password = serializer.validated_data["new_password"]

        try:
            token_obj = PasswordResetToken.objects.get(uid=password_reset_token)
        except PasswordResetToken.DoesNotExist:
            raise NotFound("Invalid password reset token")

        if token_obj.expires_at <= timezone.now():
            raise NotFound("Password reset token has expired")

        try:
            user = User.objects.get(email=token_obj.user.email)
        except User.DoesNotExist:
            raise NotFound("User with this email does not exist")

        user.set_password(new_password)
        user.save()

        # Delete OTPs + token after success
        Otp.objects.filter(user=user).delete()
        token_obj.delete()

        return success_response(
            message="Password reset successful", code=status.HTTP_200_OK
        )


class RequestOTPView(generics.CreateAPIView):
    serializer_class = RequestOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound("User with this email does not exist")

        if not user.is_active:
            raise NotFound("User account is inactive")

        # Check if user has requested OTP within the last 30 seconds
        thirty_seconds_ago = timezone.now() - timedelta(seconds=30)
        if Otp.objects.filter(user=user, created_at__gt=thirty_seconds_ago).exists():
            raise NotFound("OTP already sent.")

        otp_code = str(random.randint(1000, 9999))
        Otp.objects.create(user=user, code=otp_code)

        subject = "Your Password Reset OTP"
        message = f"Your OTP code is {otp_code}. It will expire in 5 minutes."
        send_forgot_password_otp_email.delay(subject, message, [user.email])

        return success_response(
            message="OTP sent successfully", code=status.HTTP_200_OK
        )


class VerifyOTPView(generics.CreateAPIView):
    serializer_class = VerifyOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound("User with this email does not exist")

        otp_entry = (
            Otp.objects.filter(user=user, code=otp).order_by("-created_at").first()
        )
        if not otp_entry:
            raise NotFound("Invalid OTP")

        if otp_entry.expires_at < timezone.now():
            raise NotFound("OTP has expired")

        otp_entry.delete()

        # Create and return a reset token
        reset_token = PasswordResetToken.objects.create(user=user)

        return success_response(
            message="OTP verified successfully",
            code=status.HTTP_200_OK,
            data={
                "password_reset_token": reset_token.uid,
            },
        )


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        return success_response(
            message="Password updated successfully", code=status.HTTP_200_OK
        )
