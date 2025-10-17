from django.db import models


class ProjectVisibilityChoices(models.TextChoices):
    PRIVATE = "private", "Private"
    PUBLIC = "public", "Public"
    INTERNAL = "internal", "Internal"


class ProjectStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"
    COMPLETED = "completed", "Completed"
    ON_HOLD = "on_hold", "On Hold"
    

