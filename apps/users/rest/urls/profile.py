from django.urls import path

from apps.users.rest.views.profile import UserProfileDetailView

urlpatterns = [
    path("", UserProfileDetailView.as_view(), name="user-profile-detail"),
]
