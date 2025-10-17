from django.db import models


class OrganizationMemberRoleChoices(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"
    PROJECT_MANAGER = "manager", "Manager"
