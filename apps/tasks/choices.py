from django.db import models


class TasksPriorityChoices(models.TextChoices):
    HIGH = "high", "High"
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
