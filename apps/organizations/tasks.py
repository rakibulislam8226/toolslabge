from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task


@shared_task
def send_invitation_email(email, accept_url, organization_name):
    subject = f"You've been invited to join {organization_name}"

    message = f"""
        Hi,

        You have been invited to join {organization_name}.

        Click the link below to accept your invitation:
        {accept_url}

        If you didn't expect this, you can ignore the email.

        Thanks,
        {organization_name} Team
        """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
