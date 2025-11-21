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
        keep_attachment_ids = request.data.getlist("keep_attachment_ids[]")
        process_attachments = request.data.get("process_attachments") == "true"

        # Convert string IDs to integers if they exist
        if keep_attachment_ids:
            try:
                keep_attachment_ids = [
                    int(id_str) for id_str in keep_attachment_ids if id_str.strip()
                ]
            except ValueError:
                keep_attachment_ids = []

        if attachments_data or keep_attachment_ids or process_attachments:
            TasksCommentAttachments.objects.filter(comment=instance).exclude(
                id__in=keep_attachment_ids
            ).delete()

            # Create new attachments from uploaded files
            for attachment_file in attachments_data:
                TasksCommentAttachments.objects.create(
                    comment=instance,
                    file=attachment_file,
                )

        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
