from django.urls import path

from ..views.projects import ProjectListCreateView, ProjectMemberListCreateView

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path(
        "project-members/",
        ProjectMemberListCreateView.as_view(),
        name="project-member-list-create",
    ),
]
