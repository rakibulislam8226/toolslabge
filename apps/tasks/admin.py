from django.contrib import admin

from .models import Task, TaskStatus, TaskComment, TaskAttachment, TaskHistory


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "assigned_to", "due_date", "priority")
    search_fields = ("title", "description")
    list_filter = ("status", "priority", "due_date")
    ordering = ("-created_at",)


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("organization", "name")


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at")
    search_fields = ("task__title", "author__username", "content")
    ordering = ("-created_at",)


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "created_at",
    )
    search_fields = ("task__title",)
    ordering = ("-created_at",)


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("task", "updated_at", "changed_by")
    search_fields = ("task__title", "changed_by__username", "change_description")
    ordering = ("-updated_at",)
