from django.db import models


class TasksPriorityChoices(models.TextChoices):
    HIGH = "high", "High"
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"


class TasksActivityTypeChoices(models.TextChoices):
    CREATED = "created", "Created"
    UPDATED = "updated", "Updated"
    DELETED = "deleted", "Deleted"
    COMMENTED = "commented", "Commented"
    ATTACHED_FILE = "attached_file", "Attached File"
    CHANGED_STATUS = "changed_status", "Changed Status"
    CHANGED_PRIORITY = "changed_priority", "Changed Priority"
    ASSIGNED_MEMBER = "assigned_member", "Assigned Member"
    REMOVED_MEMBER = "removed_member", "Removed Member"
