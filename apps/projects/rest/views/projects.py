from django.db.models import Q

from rest_framework import generics, permissions

from ..serializers.projects import ProjectListSerializer, ProjectMemberSerializer
from ...models import Project, ProjectMember

from ....organizations.permissions import IsOrgOwnerAdminOrManager


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(organization__memberships__user=user) | Q(memberships__user=user)
        ).distinct()


class ProjectMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsOrgOwnerAdminOrManager]

    def get_queryset(self):
        return ProjectMember.objects.filter(
            project__organization__memberships__user=self.request.user
        )
