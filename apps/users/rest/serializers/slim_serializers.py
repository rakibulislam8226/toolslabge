from rest_framework import serializers

from ...models import User


class UserSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "photo",
        ]
