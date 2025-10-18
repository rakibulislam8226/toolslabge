from django.contrib import admin

from .models import (
    Task,
    TaskStatus,
    TaskComment,
    TaskAttachment,
    TaskActivity,
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


@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = ("task", "updated_at", "created_by", "action")
    search_fields = ("task__title", "created_by__username", "details")
    ordering = ("-updated_at",)
