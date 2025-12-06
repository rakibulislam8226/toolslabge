from rest_framework import serializers
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

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
        if "photo" in validated_data and validated_data["photo"]:
            photo = validated_data["photo"]
            img = Image.open(photo)
            img = img.resize((100, 100), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format="JPEG", quality=95)
            output.seek(0)
            validated_data["photo"] = ContentFile(
                output.read(), name=f"{photo.name.split('.')[0]}_100x100.jpg"
            )

        return super().update(instance, validated_data)
