from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel

from .choices import OrganizationMemberRoleChoices


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    billing_customer_id = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class OrganizationMember(TimeStampedModel):
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
        choices=OrganizationMemberRoleChoices.choices,
        default=OrganizationMemberRoleChoices.MEMBER,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "organization")
        indexes = [models.Index(fields=["organization", "role"])]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"


class OrganizationInvitation(TimeStampedModel):
    email = models.EmailField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="invitations"
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_organization_invitations",
    )
    role = models.CharField(
        max_length=100,
        choices=OrganizationMemberRoleChoices.choices,
        default=OrganizationMemberRoleChoices.MEMBER,
    )
    token = models.CharField(max_length=64, unique=True)
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("email", "organization")

    def accept(self, user):
        if not self.accepted:
            OrganizationMember.objects.create(
                user=user,
                organization=self.organization,
                role=OrganizationMemberRoleChoices.MEMBER,
            )
            self.accepted = True
            self.accepted_at = timezone.now()
            self.save()

    def __str__(self):
        return f"Invitation for {self.email} to join {self.organization}"
