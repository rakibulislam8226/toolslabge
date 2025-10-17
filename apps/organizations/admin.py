from django.contrib import admin

from .models import Organization


# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "deleted_at",
    )
    search_fields = ("name",)
    list_filter = ("is_active", "created_at")
    ordering = ("-created_at",)
