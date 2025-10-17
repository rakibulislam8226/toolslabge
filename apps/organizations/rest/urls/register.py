from django.urls import path

from ..views.register import RegisterOrganizationOwnerView

urlpatterns = [
    path(
        "owner/",
        RegisterOrganizationOwnerView.as_view(),
        name="register_organization_owner",
    ),
]
