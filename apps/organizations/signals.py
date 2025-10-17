from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.tasks.models import TaskStatus

from .models import Organization


@receiver(post_save, sender=Organization)
def create_default_task_statuses(sender, instance, created, **kwargs):
    if created:
        default_statuses = [
            ("To Do", 1, True),
            ("In Progress", 2, False),
            ("Review", 3, False),
            ("Done", 4, False),
            ("Closed", 5, False),
        ]
        for name, position, is_default in default_statuses:
            TaskStatus.objects.get_or_create(
                organization=instance,
                name=name,
                defaults={
                    "position": position,
                    "is_default": is_default,
                },
            )
