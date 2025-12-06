from django.urls import path, include

urlpatterns = [
    path("profile/", include("apps.users.rest.urls.profile")),
    path("my-info/", include("apps.users.rest.urls.my_info")),
    path("email/", include("apps.users.rest.urls.verification")),
    path("password-reset/", include("apps.users.rest.urls.password_reset")),
]
