from django.contrib import admin

from .models import Organization, OrganizationMember, OrganizationInvitation


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


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = (
        "user__email",
        "organization",
        "role",
        "is_active",
        "joined_at",
        "deleted_at",
    )
    search_fields = ("user__username", "organization__name", "role")
    list_filter = ("organization", "role", "is_active", "joined_at")
    ordering = ("-joined_at",)


@admin.register(OrganizationInvitation)
class OrganizationInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "organization",
        "role",
        "created_at",
        "deleted_at",
    )
    search_fields = ("email", "organization__name", "role")
    list_filter = ("role", "created_at")
    ordering = ("-created_at",)
