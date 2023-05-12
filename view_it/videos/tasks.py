from config import celery_app
from view_it.videos.models import Videos


@celery_app.task()
def generate_thumbnail(video_id: int):
    """
    Asynchronous task to create a thumbnail from a video file using ffmpeg.
    """
    video = Videos.objects.get(id=video_id)
    return video.create_thumbnail()
