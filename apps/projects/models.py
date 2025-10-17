from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel

from apps.organizations.models import Organization


from .choices import ProjectVisibilityChoices, ProjectStatusChoices


class Project(TimeStampedModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(null=True, blank=True)
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
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
