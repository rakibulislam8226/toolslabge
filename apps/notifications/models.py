from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel

from apps.organizations.models import Organization


class Notification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="+"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
