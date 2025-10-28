from django.db.models import Q

from rest_framework import generics, permissions

from ..serializers.projects import (
    ProjectListSerializer,
    ProjectMemberSerializer,
    ProjectDetailSerializer,
)
from ...models import Project, ProjectMember

from ....organizations.permissions import IsOrgOwnerAdminOrManager


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects.select_related("organization")
            .filter(organization=user.organization_memberships.first().organization)
            .distinct()
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects.select_related("organization")
            .filter(organization=user.organization_memberships.first().organization)
            .distinct()
        )


class ProjectMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        # project_id = self.kwargs.get("project_id")
        project_slug = self.kwargs.get("slug")
        search = self.request.query_params.get("search", "")
        qs = ProjectMember.objects.select_related("project", "user").filter(
            project__organization=user.organization_memberships.first().organization,
            project__slug=project_slug,
        )
        if search:
            qs = qs.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__email__icontains=search)
            )
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_slug"] = self.kwargs.get("slug")
        return context


class ProjectMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]
    lookup_field = "id"


    def get_queryset(self):
        user = self.request.user
        project_slug = self.kwargs.get("slug")
        return ProjectMember.objects.select_related("project", "user").filter(
            project__organization=user.organization_memberships.first().organization,
            project__slug=project_slug,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_slug"] = self.kwargs.get("slug")
        return context
