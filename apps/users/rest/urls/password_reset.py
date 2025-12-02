from django.urls import path

from apps.users.rest.views.password_reset import (
    RequestOTPView,
    VerifyOTPView,
    PasswordResetView,
    UpdatePasswordView,
)


urlpatterns = [
    path("", PasswordResetView.as_view(), name="update-password"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path(
        "request/",
        RequestOTPView.as_view(),
        name="request-otp",
    ),
    path(
        "update-password/",
        UpdatePasswordView.as_view(),
        name="update-password",
    ),
]
