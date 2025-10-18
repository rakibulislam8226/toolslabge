from django.urls import path

from ..views.members import OrganizationMembersListView

urlpatterns = [
    path(
        "<int:org_id>/members/",
        OrganizationMembersListView.as_view(),
        name="list-members",
    ),
]
