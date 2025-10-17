from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel

from .choices import OrganizationMembershipRoleChoices


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    billing_customer_id = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class OrganizationMembership(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=100,
        choices=OrganizationMembershipRoleChoices.choices,
        default=OrganizationMembershipRoleChoices.MEMBER,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "organization")
        indexes = [models.Index(fields=["organization", "role"])]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"
