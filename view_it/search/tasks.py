from config import celery_app
from view_it.search.models import Search


@celery_app.task()
def add_video_to_search_index(video_id: int):
    """
    Asynchronous task to add a video to the MeiliSearch index.
    """
    search = Search()
    return search.add_video(video_id=video_id)


@celery_app.task()
def add_user_to_search_index(user_id: int):
    """
    Asynchronous task to add a user to the MeiliSearch index.
    """
    search = Search()
    return search.add_user(user_id=user_id)
