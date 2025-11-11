from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField

from common.models import TimeStampedModel

from apps.organizations.models import Organization
from apps.projects.models import Project, ProjectMember

from .choices import TasksPriorityChoices, TasksActivityTypeChoices


class TaskStatus(TimeStampedModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="task_statuses"
    )
    slug = AutoSlugField(populate_from="name", unique=True)
    position = models.PositiveSmallIntegerField(default=0)  # for ordering in UI
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "slug")
        ordering = ["organization", "name"]

    def __str__(self):
        return self.name


class Task(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="tasks"
    )
    status = models.ForeignKey(
        TaskStatus, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=TasksPriorityChoices.choices,
        default=TasksPriorityChoices.MEDIUM,
    )
    estimated_hours = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TaskDeadlineExtension(TimeStampedModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="deadline_extensions"
    )
    previous_due_date = models.DateTimeField()
    new_due_date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Extension of Task {self.task.id} to {self.new_due_date}"


class TaskMember(TimeStampedModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="task_members"
    )
    member = models.ForeignKey(
        ProjectMember,
        on_delete=models.CASCADE,
        related_name="member_tasks",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "member")

    def __str__(self):
        return f"{self.member} assigned to {self.task}"


class TaskComment(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task_comments"
    )
    content = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"


class TaskAttachment(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_attachments",
    )
    file = models.FileField(upload_to="task_attachments/")
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Attachment for {self.task} by {self.uploaded_by}"


class TaskActivity(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activity")
    action = models.CharField(
        max_length=50,
        choices=TasksActivityTypeChoices.choices,
    )
    details = models.TextField(blank=True, null=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["task", "created_at"])]

    def __str__(self):
        return f"History for {self.task} by {self.changed_by}"
