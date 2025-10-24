from django.urls import path

from ..views.members import OrganizationMembersListView, MyOrganizationMembersListView

urlpatterns = [
    path(
        "members/",
        MyOrganizationMembersListView.as_view(),
        name="my-organization-members",
    ),
    path(
        "<int:org_id>/members/",
        OrganizationMembersListView.as_view(),
        name="list-members",
    ),
]
