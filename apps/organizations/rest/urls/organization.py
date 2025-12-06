from django.urls import path

from ..views.organization import RegisterOrganizationView, OrganizationDetailView

urlpatterns = [
    path(
        "",
        OrganizationDetailView.as_view(),
        name="detail-organization",
    ),
    path(
        "register/",
        RegisterOrganizationView.as_view(),
        name="register_organization",
    ),
]
