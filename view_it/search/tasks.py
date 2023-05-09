from config import celery_app
from config.meilisearch_client import meilisearch_client
from view_it.videos.models import Videos


@celery_app.task()
def add_video_to_search_index(video_id: int):
    video = Videos.objects.get(id=video_id)

    description = ""
    if video.description:
        description = video.description

    thumbnail = ""
    if video.thumbnail:
        thumbnail = video.thumbnail.url

    document = {
        "id": video.id,
        "url_slug": str(video.url_slug),
        "title": video.title,
        "description": description,
        "url": str(video.get_absolute_url()),
        "user": video.user.username,
        "thumbnail": thumbnail,
    }

    try:
        meilisearch_client.index("videos").add_documents(document)
    except meilisearch_client.error as error:
        raise error

    return meilisearch_client.get_task(0)
