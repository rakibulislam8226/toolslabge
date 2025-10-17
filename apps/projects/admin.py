from django.contrib import admin

from .models import Project, ProjectMember

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "visibility",
        "status",
    )
    list_filter = ("visibility", "status", "organization")
    search_fields = ("name", "description")
    ordering = ("-created_at",)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "role",
    )
    list_filter = ("role", "project")
    search_fields = ("user__username", "user__email", "project__name")
    ordering = ("-created_at",)
