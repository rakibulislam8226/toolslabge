from django.urls import path, include

urlpatterns = [
    path("", include("apps.organizations.rest.urls.invitations")),
    path("", include("apps.organizations.rest.urls.members")),
    path("", include("apps.organizations.rest.urls.organization")),
]
