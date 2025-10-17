from django.urls import path, include

urlpatterns = [
    path("", include("apps.organizations.rest.urls.invitations")),
    path("register/", include("apps.organizations.rest.urls.register")),
]
