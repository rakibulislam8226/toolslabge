from rest_framework import serializers
import json

from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from apps.tasks.models import TaskComment, Task, TasksCommentAttachments
from apps.users.models import User


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
    mentions = serializers.JSONField(required=False)

    class Meta:
        model = TaskComment
        fields = [
            "id",
            "content",
            "attachment",
            "mentions",
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
        task_id = self.context.get("task_id")
        task = Task.objects.get(id=task_id)
        author = request.user

        # Handle mentions data
        mentions_data = request.data.get("mentions")
        if mentions_data and isinstance(mentions_data, str):
            try:
                mentions_data = json.loads(mentions_data)
            except json.JSONDecodeError:
                mentions_data = []
        elif not mentions_data:
            mentions_data = []

        comment = TaskComment.objects.create(
            task=task,
            author=author,
            content=validated_data.get("content"),
            mentions=mentions_data,
        )

        # Process mentions for notifications
        if mentions_data:
            self.process_mentions(comment, mentions_data)

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

    def process_mentions(self, comment, mentions_data):
        """
        Process mentions and send notifications
        """
        for mention in mentions_data:
            user_id = mention.get("userId")
            user_email = mention.get("email")

            try:
                # Find the mentioned user
                if user_id:
                    mentioned_user = User.objects.get(id=user_id)
                elif user_email:
                    mentioned_user = User.objects.get(email=user_email)
                else:
                    continue

                # Print mention information (replace with actual notification logic)
                print(f"\n📧 MENTION DETECTED:")
                print(f"   Task: {comment.task.title}")
                print(f"   Comment by: {comment.author.email}")
                print(f"   Mentioned user: {mentioned_user.email}")
                print(f"   User ID: {mentioned_user.id}")
                print(f"   Comment content: {comment.content[:50]}...")
                print(
                    f"   Task URL: /projects/{comment.task.project.slug}/tasks/{comment.task.id}"
                )

                # TODO: Uncomment these lines to enable notifications
                # from mention_notifications_example import MentionNotificationService
                # MentionNotificationService.send_mention_email(mentioned_user, comment)
                # MentionNotificationService.create_in_app_notification(mentioned_user, comment)

            except User.DoesNotExist:
                print(f"⚠️  User not found for mention: {mention}")
                continue
