from django.contrib import admin

from .models import User, EmailVerificationToken

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "uid",
        "first_name",
        "is_active",
        "is_verified",
        "date_joined",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_verified")
    ordering = ("-date_joined",)
    readonly_fields = ("uid",)


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "token",
        "is_used",
        "expires_at",
        "created_at",
        "is_expired_status",
    )
    search_fields = ("user__email", "token")
    list_filter = ("is_used", "expires_at", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("token", "created_at", "updated_at", "is_expired_status")

    def is_expired_status(self, obj):
        return obj.is_expired()

    is_expired_status.boolean = True
    is_expired_status.short_description = "Is Expired"
