import os

import ffmpeg
from django.conf import settings
from django.core.files.base import ContentFile

from config import celery_app
from view_it.videos.models import Videos


@celery_app.task(ignore_result=True)
def create_thumbnail_from_video(video_url: str, video_id: int):
    input_file_path = os.path.join(settings.APPS_DIR, video_url.lstrip("/"))

    thumbnail_file_path = f"{os.path.dirname(input_file_path)}output.jpg"

    # Extract video metadata using ffprobe
    try:
        probe = ffmpeg.probe(input_file_path)
    except ffmpeg.Error as e:
        print(f"ffprobe stderr: {e.stderr.decode('utf-8')}")
        raise e

    duration = float(probe["format"]["duration"])
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    width = int(video_stream["width"])
    time_offset = duration / 2

    # Create the thumbnail using ffmpeg
    try:
        (
            ffmpeg.input(input_file_path, ss=time_offset)
            .filter("scale", width, -1)
            .output(thumbnail_file_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg._run.Error as e:
        raise e

    # Save the thumbnail to the video model and delete the local file
    video = Videos.objects.get(id=video_id)
    with open(thumbnail_file_path, "rb") as file:
        content_file = ContentFile(file.read(), name=thumbnail_file_path)
        video.thumbnail.save(content_file.name, content_file)

    os.remove(thumbnail_file_path)
