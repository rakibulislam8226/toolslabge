from django.db.models import Q

from rest_framework import generics, permissions

from ..serializers.projects import ProjectSerializer, ProjectMemberSerializer
from ...models import Project, ProjectMember

from ...permissions import IsOrgAdminOrManager


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsOrgAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(organization__memberships__user=user) | Q(memberships__user=user)
        ).distinct()


class ProjectMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsOrgAdminOrManager]

    def get_queryset(self):
        return ProjectMember.objects.filter(
            project__organization__memberships__user=self.request.user
        )
