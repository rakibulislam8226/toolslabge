from django.contrib import admin

from .models import (
    Task,
    TaskStatus,
    TaskComment,
    TaskAttachment,
    TaskHistory,
    TaskMember,
)


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    list_filter = ("organization",)
    search_fields = ("name",)
    ordering = ("organization", "name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "due_date", "priority")
    search_fields = ("title", "description")
    list_filter = ("status", "priority", "due_date")
    ordering = ("-created_at",)


@admin.register(TaskMember)
class TaskMemberAdmin(admin.ModelAdmin):
    list_display = ("task", "member", "assigned_at")
    search_fields = ("task__title", "member__user__username")
    ordering = ("-assigned_at",)


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
