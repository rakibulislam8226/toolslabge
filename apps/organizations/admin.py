from django.contrib import admin

from .models import Organization, OrganizationMembership


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


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "organization",
        "role",
        "is_active",
        "joined_at",
        "deleted_at",
    )
    search_fields = ("user__username", "organization__name", "role")
    list_filter = ("role", "is_active", "joined_at")
    ordering = ("-joined_at",)
