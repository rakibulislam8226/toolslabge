import uuid
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

from versatileimagefield.fields import VersatileImageField

from common.models import TimeStampedModel
from .managers import CustomUserManager

# Create your models here.


class User(AbstractUser, TimeStampedModel, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    photo = VersatileImageField(
        upload_to="user_photos/",
        null=True,
        blank=True,
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_joined = timezone.now()
        self.username = self.email
        super().save(*args, **kwargs)


class EmailVerificationToken(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verification_tokens"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["user", "is_used"]),
        ]

    def __str__(self):
        return f"Verification token for {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        return not self.is_used and not self.is_expired()


class Otp(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=4)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)


class PasswordResetToken(TimeStampedModel):
    uid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reset_tokens"
    )
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Password Reset Token for {self.user.email} - {self.uid}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)
