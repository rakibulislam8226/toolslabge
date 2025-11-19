from rest_framework import serializers

from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from apps.tasks.models import TaskComment, Task, TasksCommentAttachments


class TasksCommentAttachmentsSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksCommentAttachments
        fields = [
            "id",
            "file",
            "created_at",
            "updated_at",
        ]


class TaskCommentListSerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)
    attachment = TasksCommentAttachmentsSlimSerializer(
        source="attachments",
        many=True,
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = TaskComment
        fields = [
            "id",
            "content",
            "attachment",
            "task",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "task",
            "author",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        task = self.context.get("task")
        author = request.user

        comment = TaskComment.objects.create(
            task=task,
            author=author,
            content=validated_data.get("content"),
        )

        attachments_data = request.FILES.getlist("attachment")
        if attachments_data:
            for attachment_file in attachments_data:
                TasksCommentAttachments.objects.create(
                    comment=comment,
                    file=attachment_file,
                )

        return comment

    def update(self, instance, validated_data):
        request = self.context.get("request")
        attachments_data = request.FILES.getlist("attachment")
        if attachments_data:
            TasksCommentAttachments.objects.filter(comment=instance).delete()
            for attachment_file in attachments_data:
                TasksCommentAttachments.objects.create(
                    comment=instance,
                    file=attachment_file,
                )

        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
