from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel

from apps.organizations.models import Organization


from .choices import (
    ProjectVisibilityChoices,
    ProjectStatusChoices,
    ProjectMemberRoleChoices,
)


class Project(TimeStampedModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    visibility = models.CharField(
        max_length=50,
        choices=ProjectVisibilityChoices.choices,
        default=ProjectVisibilityChoices.PRIVATE,
    )
    status = models.CharField(
        max_length=50,
        choices=ProjectStatusChoices.choices,
        default=ProjectStatusChoices.ACTIVE,
    )

    class Meta:
        unique_together = ("organization", "name")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProjectMember(TimeStampedModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )
    role = models.CharField(
        max_length=100,
        choices=ProjectMemberRoleChoices.choices,
        default=ProjectMemberRoleChoices.CONTRIBUTOR,
    )

    class Meta:
        unique_together = ("project", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} in {self.project}"
