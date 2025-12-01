import json

from django.conf import settings

from rest_framework import serializers

from apps.users.rest.serializers.slim_serializers import UserSlimSerializer
from apps.tasks.models import TaskComment, Task, TasksCommentAttachments
from apps.users.models import User

from ...tasks import send_task_comment_mentioned_email


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

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        request = self.context.get("request")
        if request and request.method == "GET":
            rep["content"] = {
                "text": rep.get("content"),
                "mentions": rep.get("mentions"),
            }
            rep.pop("mentions", None)

        return rep

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

        comment.content = {
            "text": comment.content,
            "mentions": comment.mentions,
        }

        return comment

    def update(self, instance, validated_data):
        request = self.context.get("request")

        # Handle mentions data
        mentions_data = request.data.get("mentions")
        if mentions_data and isinstance(mentions_data, str):
            try:
                mentions_data = json.loads(mentions_data)
            except json.JSONDecodeError:
                mentions_data = []
        elif not mentions_data:
            mentions_data = []

        instance.content = validated_data.get("content", instance.content)
        instance.mentions = mentions_data
        instance.save()

        # Process mentions for notifications
        if mentions_data:
            self.process_mentions(instance, mentions_data)

        attachments_data = request.FILES.getlist("attachment")
        if attachments_data:
            for attachment_file in attachments_data:
                TasksCommentAttachments.objects.create(
                    comment=instance,
                    file=attachment_file,
                )

        instance.content = {
            "text": instance.content,
            "mentions": instance.mentions,
        }

        return instance

    def process_mentions(self, comment, mentions_data):
        """
        Process mentions and send notifications
        """
        for mention in mentions_data:
            user_id = mention.get("user")
            user_email = mention.get("email")
            user_name = mention.get("user_name")

            try:
                if user_id:
                    mentioned_user = User.objects.get(id=user_id)
                elif user_email:
                    mentioned_user = User.objects.get(email=user_email)
                elif user_name:
                    mentioned_user = User.objects.get(username=user_name)
                else:
                    continue

                print(f"   Task: {comment.task.title}")
                print(f"   Comment by: {comment.author.email}")
                print(f"   Mentioned user: {mentioned_user.email}")
                print(f"   User ID: {mentioned_user.id}")
                print(f"   Comment content: {comment.content[:50]}...")
                task_url = self.context["request"].build_absolute_uri(
                    f"/projects/{comment.task.project.slug}/tasks/?task_id={comment.task.id}"
                )
                send_task_comment_mentioned_email.delay(
                    first_name=mentioned_user.first_name,
                    email=mentioned_user.email,
                    task_title=comment.task.title,
                    task_url=task_url,
                    mentioned_by=comment.author.get_full_name()
                    or comment.author.username,
                    project_name=comment.task.project.name,
                )

                # TODO: Uncomment these lines to enable notifications
                # from mention_notifications_example import MentionNotificationService
                # MentionNotificationService.send_mention_email(mentioned_user, comment)
                # MentionNotificationService.create_in_app_notification(mentioned_user, comment)

            except User.DoesNotExist:
                print(f"⚠️  User not found for mention: {mention}")
                continue
