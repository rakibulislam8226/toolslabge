from django.urls import path

from ..views.verification import (
    verify_email,
    resend_verification_email,
    check_verification_status,
)

urlpatterns = [
    path("verify/", verify_email, name="verify-email"),
    path("resend-verification/", resend_verification_email, name="resend-verification"),
    path(
        "status/<str:email>/",
        check_verification_status,
        name="check-verification-status",
    ),
]
