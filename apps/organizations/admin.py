from django.contrib import admin

from .models import Organization, OrganizationMembership, OrganizationInvitation


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


@admin.register(OrganizationInvitation)
class OrganizationInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "organization",
        "invited_by",
        "role",
        "created_at",
        "deleted_at",
    )
    search_fields = ("email", "organization__name", "invited_by__username", "role")
    list_filter = ("role", "created_at")
    ordering = ("-created_at",)
