import os
import subprocess
from io import BytesIO

import ffmpeg
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

from view_it.videos.models import Videos


def create_thumbnail_from_video(video_id: int, video_url: str):
    """
    Create a thumbnail from a video file using ffmpeg.
    """
    # Create the full path to the input video file
    input_file_path = os.path.join(settings.APPS_DIR, video_url.lstrip("/"))

    print(f"VIDEO_URL_IN_UTILS: {video_url}")
    print(f"INPUT FILE PATH: {input_file_path}")

    # Create the path to the output thumbnail file
    thumbnail_file_path = f"{os.path.dirname(input_file_path)}/output.jpg"

    # Extract video metadata using ffprobe
    try:
        probe = ffmpeg.probe(input_file_path)
    except ffmpeg.Error as error:
        # Log the error and re-raise it
        print(f"ffprobe stderr: {error.stderr.decode('utf-8')}")
        raise error

    # Calculate the time offset for the thumbnail and get the video width
    duration = float(probe["format"]["duration"])
    time_offset = duration / 2
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    width = int(video_stream["width"])

    # Create the thumbnail using ffmpeg
    try:
        (
            ffmpeg.input(input_file_path, ss=time_offset)
            .filter("scale", width, -1)
            .output(thumbnail_file_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as error:
        # If there's an error, re-raise it so that it can be handled elsewhere
        raise error

    # Retrieve the video from the database
    video = Videos.objects.get(id=video_id)

    # Open the thumbnail file and create a Django ContentFile from it
    with open(thumbnail_file_path, "rb") as file:
        content_file = ContentFile(file.read(), name=thumbnail_file_path)

    # Save the thumbnail to the video model
    video.thumbnail.save(content_file.name, content_file)

    # Delete the local thumbnail file now that it's been saved to the model
    os.remove(thumbnail_file_path)

    return True


def create_test_image(output_dir: str, output_file_type: str) -> SimpleUploadedFile:
    fake = Faker()

    # Generate a random image using Pillow and Faker
    image = Image.new(mode="RGB", size=(200, 200), color=fake.color_name())
    image_bytes = BytesIO()
    image.save(image_bytes, format=output_file_type.upper())

    # Set up the output file path
    file_name = "test." + output_file_type
    output_file_path = os.path.join(output_dir, file_name)

    # Save the image to the output file path
    with open(output_file_path, "wb") as f:
        f.write(image_bytes.getvalue())

    # Create the SimpleUploadedFile object and set the content type
    return SimpleUploadedFile(
        file_name, content=open(output_file_path, "rb").read(), content_type=f"image/{output_file_type}"
    )


def create_test_video(output_dir: str, output_file_type: str) -> SimpleUploadedFile:
    # Specify the appropriate codecs and content type for the output file type
    codec_map = {
        "mp4": {"v": "libx264", "a": "copy", "type": "video/mp4"},
        "ogg": {"v": "libtheora", "a": "libvorbis", "type": "video/ogg"},
        "webm": {"v": "libvpx", "a": "libvorbis", "type": "video/webm"},
        "avi": {"v": "libxvid", "a": "copy", "type": "video/avi"},
    }
    if output_file_type not in codec_map:
        raise ValueError(f"Unsupported file type: {output_file_type}")
    codec_v, codec_a, content_type = codec_map[output_file_type].values()

    # Set up the output file path and name
    output_file_name = f"test_video.{output_file_type}"
    output_file_path = os.path.join(output_dir, output_file_name)

    # Generate the test video using FFmpeg
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=5:size=320x240:rate=30",
            "-c:v",
            codec_v,
            "-preset",
            "slow",
            "-crf",
            "22",
            "-c:a",
            codec_a,
            output_file_path,
        ]
    )

    # Return the output file as a SimpleUploadedFile
    with open(output_file_path, "rb") as f:
        return SimpleUploadedFile(output_file_name, f.read(), content_type=content_type)
