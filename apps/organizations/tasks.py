from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task


@shared_task
def send_invitation_email(email, accept_url, organization_name):
    subject = f"You've been invited to join {organization_name}"

    html_message = f"""
        <p>Hi Dear,</p>
        <p>You have been invited to join {organization_name}.</p>
        <p>
            <a href="{accept_url}" style="display:inline-block;padding:10px 20px;background-color:#007bff;color:#fff;text-decoration:none;border-radius:4px;">
                Click here to accept your invitation
            </a>
        </p>
        <p>
            Or click the link below:<br>
            <a href="{accept_url}">{accept_url}</a>
        </p>
        <p>If you didn't expect this, you can ignore the email.</p>
        <p>Thanks,<br>{organization_name}</p>
    """

    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message,
    )
