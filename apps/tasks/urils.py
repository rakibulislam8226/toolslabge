from .models import TaskActivity


def log_task_activity(task, user, action, old_value=None, new_value=None, details=None):

    TaskActivity.objects.create(
        task=task,
        user=user,
        action=action,
        old_value=old_value,
        new_value=new_value,
        details=details,
    )
