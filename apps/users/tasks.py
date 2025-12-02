from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta

from celery import shared_task

from .models import User, EmailVerificationToken


@shared_task
def send_verification_email(user_id, base_url):
    """Send email verification to user"""
    try:
        user = User.objects.get(id=user_id)

        # Create verification token (expires in 24 hours)
        expires_at = timezone.now() + timedelta(hours=24)
        verification_token = EmailVerificationToken.objects.create(
            user=user, expires_at=expires_at
        )

        # Construct verification URL
        verification_url = f"{base_url}/verify-email/{verification_token.token}"

        subject = "Email Verification Required"

        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Email Verification</h2>
                <p>Hello {user.first_name or user.email},</p>
                <p>Please verify your email address to activate your account:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="display:inline-block;padding:12px 30px;background-color:#3498db;color:#fff;text-decoration:none;border-radius:5px;font-weight:bold;">
                        Verify Email
                    </a>
                </div>
                <p>This link expires in 24 hours. If you didn't create this account, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">Link: {verification_url}</p>
            </div>
        </body>
        </html>
        """

        plain_message = f"""
        Email Verification Required
        
        Hello {user.first_name or user.email},
        
        Please verify your email address to activate your account.
        
        Verification link: {verification_url}
        
        This link expires in 24 hours.
        
        If you didn't create this account, please ignore this email.
        """

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=html_message,
        )

        return f"Verification email sent to {user.email}"

    except User.DoesNotExist:
        return f"User with id {user_id} not found"
    except Exception as e:
        return f"Failed to send verification email: {str(e)}"


@shared_task
def cleanup_expired_tokens():
    """Clean up expired verification tokens"""
    expired_tokens = EmailVerificationToken.objects.filter(
        expires_at__lt=timezone.now()
    )
    count = expired_tokens.count()
    expired_tokens.delete()
    return f"Cleaned up {count} expired verification tokens"


@shared_task
def send_forgot_password_otp_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        None,
        recipient_list,
        fail_silently=False,
    )
