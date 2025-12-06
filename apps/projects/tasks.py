import logging
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

from apps.tasks.models import TaskComment, Task
from apps.users.models import User
from .utils import process_users_in_bulk


CHUNK_SIZE = 50
logging = logging.getLogger(__name__)


@shared_task
def send_task_assignment_email(
    first_name, email, task_title, task_url, created_by, project_name
):
    subject = f"You've been assigned a new task in {project_name}"

    html_message = f"""
        <p>Hi {first_name if first_name else "Dear"},</p>
        <p>You have been assigned a new task: <strong>{task_title}</strong> in the project <strong>{project_name}</strong>.</p>
        <p>
            <a href="{task_url}" style="display:inline-block;padding:10px 20px;background-color:#28a745;color:#fff;text-decoration:none;border-radius:4px;">
                View Task
            </a>
        </p>
        <p>
            Or click the link below:<br>
            <a href="{task_url}">{task_url}</a>
        </p>
        <p>If you have any questions, please contact with {created_by}.</p>
        <p>Thanks,<br>{project_name} Team</p>
    """

    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message,
    )


@shared_task
def process_task_assignment_users(task_id, user_ids, task_url):
    try:
        task = Task.objects.select_related("project", "created_by").get(id=task_id)
    except Task.DoesNotExist:
        return

    process_users_in_bulk(
        user_ids,
        task.created_by_id,
        send_task_assignment_email,
        task.title,
        task_url,
        task.created_by.get_full_name() or task.created_by.username,
        task.project.name,
    )


@shared_task
def send_member_remove_task_email(first_name, email, task_title, project_name):
    subject = f"You've been removed from a task in {project_name}"

    html_message = f"""
        <p>Hi {first_name if first_name else "Dear"},</p>
        <p>You have been removed from the task: <strong>{task_title}</strong> in the project <strong>{project_name}</strong>.</p>
        <p>If you have any questions, please contact with project manager.</p>
        <p>Thanks,<br>{project_name} Team</p>
    """

    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message,
    )


@shared_task
def process_task_member_removal(task_id, user_ids, remover_id):
    try:
        task = Task.objects.select_related("project").get(id=task_id)
    except Task.DoesNotExist:
        return

    process_users_in_bulk(
        user_ids,
        remover_id,
        send_member_remove_task_email,
        task.title,
        task.project.name,
    )


@shared_task
def send_task_comment_mentioned_email(
    first_name, email, task_title, task_url, mentioned_by, project_name
):
    subject = f"You were mentioned in a comment on a task in {project_name}"

    html_message = f"""
        <p>Hi {first_name if first_name else "Dear"},</p>
        <p>You were mentioned by <strong>{mentioned_by}</strong> in a comment on the task: <strong>{task_title}</strong> in the project <strong>{project_name}</strong>.</p>
        <p>
            <a href="{task_url}" style="display:inline-block;padding:10px 20px;background-color:#007bff;color:#fff;text-decoration:none;border-radius:4px;">
                View Task
            </a>
        </p>
        <p>
            Or click the link below:<br>
            <a href="{task_url}">{task_url}</a>
        </p>
        <p>If you have any questions, please contact with project manager.</p>
        <p>Thanks,<br>{project_name} Team</p>
    """

    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message,
    )


@shared_task
def chunk_wise_process_comment_mentions(comment_id, user_ids, task_url):
    try:
        comment = TaskComment.objects.select_related("task__project", "author").get(
            id=comment_id
        )
    except TaskComment.DoesNotExist:
        return

    process_users_in_bulk(
        user_ids,
        comment.author.id,
        send_task_comment_mentioned_email,
        comment.task.title,
        task_url,
        comment.author.get_full_name() or comment.author.username,
        comment.task.project.name,
    )
