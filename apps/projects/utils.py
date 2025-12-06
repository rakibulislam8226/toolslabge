from django.contrib.auth import get_user_model

User = get_user_model()

CHUNK_SIZE = 50


def process_users_in_bulk(user_ids, skip_id, child_task, *extra_args):
    """
    Fully reusable user bulk processor:
    - Loads users
    - Converts to list
    - Splits into chunks
    - Skips specific user
    - Calls Celery child task

    :param user_ids: list of user IDs to process
    :param skip_id: user ID to skip (e.g., author, task creator)
    :param child_task: Celery task function to call for each user
    :param extra_args: extra args for child task
    """

    # Load users
    users = User.objects.filter(id__in=user_ids).values("id", "first_name", "email")
    if not users.exists():
        return

    # Convert to list
    users_list = list(users)

    # Chunking handled here
    for i in range(0, len(users_list), CHUNK_SIZE):
        chunk = users_list[i : i + CHUNK_SIZE]

        for user in chunk:
            if user["id"] == skip_id:
                continue  # skip author/creator

            # Send email via child Celery task
            child_task.delay(user["first_name"], user["email"], *extra_args)
