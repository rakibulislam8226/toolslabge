from django.contrib import admin

from .models import Notification

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "title", "is_read")
    list_filter = ("is_read",)
    search_fields = ("title", "body", "user__username", "organization__name")
