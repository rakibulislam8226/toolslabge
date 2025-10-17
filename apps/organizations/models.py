from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    billing_customer_id = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
