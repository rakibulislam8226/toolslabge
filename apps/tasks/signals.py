from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Task, TaskStatusHistory


@receiver(pre_save, sender=Task)
def track_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_task = Task.objects.get(pk=instance.pk)
    changed_by = getattr(instance, "_changed_by", None)
    if old_task.status != instance.status:
        TaskStatusHistory.objects.create(
            task=instance,
            previous_status=old_task.status,
            new_status=instance.status,
            changed_by=changed_by,
        )
