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


class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

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
        project_id = self.kwargs.get("project_id")
        return ProjectMember.objects.select_related("project", "user").filter(
            project__organization=user.organization_memberships.first().organization,
            project__id=project_id,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_id"] = self.kwargs.get("project_id")
        return context
