from rest_framework import serializers

from apps.users.models import User


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "photo",
        ]
        read_only_fields = ["id", "email", "username"]

    def update(self, instance, validated_data):
        validated_data.pop("email", None)
        validated_data.pop("username", None)
        return super().update(instance, validated_data)
