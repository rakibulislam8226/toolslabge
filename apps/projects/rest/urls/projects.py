from django.urls import path

from ..views.projects import (
    ProjectListCreateView,
    ProjectDetailView,
    ProjectMemberListCreateView,
    ProjectMemberDetailView,
)

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    # path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<slug:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path(
        "<slug:slug>/members/",
        ProjectMemberListCreateView.as_view(),
        name="project-member-list-create",
    ),
    path(
        "<slug:slug>/members/<int:id>/",
        ProjectMemberDetailView.as_view(),
        name="project-member-detail",
    ),
]
