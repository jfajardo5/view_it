from django.contrib.auth import get_user_model

from config import celery_app
from config.meilisearch_client import meilisearch_client
from view_it.videos.models import Videos

# Get the User model
User = get_user_model()


@celery_app.task()
def add_video_to_search_index(video_id: int):
    """
    Asynchronous task to add a video to the MeiliSearch index.
    """
    # Retrieve the video from the database
    video = Videos.objects.get(id=video_id)

    # Prepare the video's data for the search index
    document = {
        "id": video.id,
        "url_slug": str(video.url_slug),
        "title": video.title,
        "description": video.description if video.description else "",
        "url": str(video.get_absolute_url()),
        "user": video.user.username,
        "thumbnail": video.thumbnail.url if video.thumbnail else "",
    }

    # Try to add the video to the MeiliSearch index
    try:
        meilisearch_client.index("videos").add_documents([document])
    except meilisearch_client.error as error:
        # If there's an error, raise it so that it can be handled elsewhere
        raise error

    # Return the MeiliSearch task
    return meilisearch_client.get_task(0)


@celery_app.task()
def add_user_to_search_index(id: int):
    """
    Asynchronous task to add a user to the MeiliSearch index.
    """
    # Retrieve the user from the database
    user = User.objects.get(id=id)

    # Prepare the user's data for the search index
    document = {
        "id": user.id,
        "username": user.username,
        "description": user.channel_description if user.channel_description else "",
        "avatar_url": user.avatar.url if user.avatar else "",
        "url": str(user.get_absolute_url()),
    }

    # Try to add the user to the MeiliSearch index
    try:
        meilisearch_client.index("users").add_documents([document])
    except meilisearch_client.error as error:
        # If there's an error, raise it so that it can be handled elsewhere
        raise error

    # Return the MeiliSearch task
    return meilisearch_client.get_task(0)
