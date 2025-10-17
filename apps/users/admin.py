from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "uid",
        "first_name",
        "is_active",
        "date_joined",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active")
    ordering = ("-date_joined",)
    readonly_fields = ("uid",)
