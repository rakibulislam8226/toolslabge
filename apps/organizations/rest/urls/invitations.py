from django.urls import path

from ..views.invitations import SendInvitationView, AcceptInvitationView

urlpatterns = [
    path(
        "<int:org_id>/invite/",
        SendInvitationView.as_view(),
        name="send-invite",
    ),
    path("accept-invite/", AcceptInvitationView.as_view(), name="accept-invite"),
]
