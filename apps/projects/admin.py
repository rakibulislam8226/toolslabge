from django.contrib import admin

from .models import Project

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
