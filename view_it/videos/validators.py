import magic
from django.core.exceptions import ValidationError


def validate_video_file_type(value):
    """
    Validator that verifies video's file type.
    """
    allowed_types = [
        "video/mp4",  # MP4 (MPEG-4 Part 14)
        "video/webm",  # WebM (VP8/VP9)
        "video/ogg",  # Ogg (Theora/Vorbis)
    ]
    try:
        file_type = magic.from_buffer(value.read(), mime=True)
    except file_type not in allowed_types:
        raise ValidationError

    return


def validate_video_thumbnail_file_type(value):
    """
    Validator that verifies video thumbnail's file type.
    """
    allowed_types = [
        "image/jpeg",  # JPEG/JPG (Joint Photographic Experts Group)
        "image/png",  # PNG (Portable Network Graphics)
        "image/gif",  # GIF (Graphics Interchange Format)
    ]
    try:
        file_type = magic.from_buffer(value.read(), mime=True)
    except file_type not in allowed_types:
        raise ValidationError

    return
