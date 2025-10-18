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
