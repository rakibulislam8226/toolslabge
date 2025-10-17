from django.urls import path

from ..views.register import RegisterOrganizationView

urlpatterns = [
    path(
        "",
        RegisterOrganizationView.as_view(),
        name="register_organization",
    ),
]
