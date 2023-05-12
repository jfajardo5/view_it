import os
import subprocess
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image


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
