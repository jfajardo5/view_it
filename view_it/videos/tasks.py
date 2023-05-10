from config import celery_app
from view_it.utils.videos_utils import create_thumbnail_from_video


@celery_app.task()
def generate_thumbnail(video_id: int, video_url: str):
    """
    Asynchronous task to create a thumbnail from a video file using ffmpeg.
    """
    result = create_thumbnail_from_video(video_id=video_id, video_url=video_url)
    return result
