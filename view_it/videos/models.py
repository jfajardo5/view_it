import os
import uuid

import ffmpeg
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .validators import validate_video_file_type, validate_video_thumbnail_file_type

# Get the user model
User = get_user_model()


def upload_to(instance, filename):
    """
    Function to generate a unique path for each uploaded file.
    Files are stored in a directory structure by date and time with a randomly generated string for the filename.
    """
    _, filename_ext = os.path.splitext(filename)
    now = timezone.now()
    date_string = now.strftime(f"%Y/%m/%d/%H/{get_random_string(20)}{filename_ext}")
    return date_string


class Videos(models.Model):
    """
    Model to represent a video.
    """

    # Video visibility options
    PUBLIC = "public"
    PRIVATE = "private"

    STATUS_CHOICES = (
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
    )

    # Fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    url_slug = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(
        _("Video Title"),
        max_length=200,
        null=False,
        blank=False,
    )

    description = models.TextField(
        _("Video Description"),
        null=True,
        blank=True,
    )

    file = models.FileField(
        _("Video File Path"),
        upload_to=upload_to,
        null=False,
        blank=False,
        validators=[validate_video_file_type],
        help_text=_("Required. Supported file types are: .mp4, .webm, and .ogv"),
    )

    thumbnail = models.FileField(
        _("Thumbnail File Path"),
        upload_to=upload_to,
        null=True,
        blank=True,
        validators=[validate_video_thumbnail_file_type],
        help_text=_("Required. Supported file types are: .jpg, .jpeg, .png, and .gif"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="public",
        null=False,
        blank=False,
    )

    uploaded_timestamp = models.DateTimeField(
        _("Video Upload Timestamp"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """Get URL for videos' detail view.

        Returns:
            str: URL for videos detail.

        """
        return reverse("videos:detail", kwargs={"url_slug": self.url_slug})

    def create_thumbnail(self):
        """
        Create a thumbnail from a video file using ffmpeg.

        This function generates a thumbnail at the middle of the video duration and scales it
        according to the video's original width. The generated thumbnail is then saved to the `thumbnail` field
        of the video instance and the local file is deleted.

        ***Warning*** Creating a thumbnail from a video file is a CPU-intensive process
        and inherently requires a fair amount of computational resources.
        """

        # Define the path for the input video file
        input_file_path = os.path.join(settings.APPS_DIR, self.file.url.lstrip("/"))

        # Define the path for the output thumbnail file
        thumbnail_file_path = f"{os.path.dirname(input_file_path)}/output.jpg"

        # Extract video metadata using ffprobe
        try:
            probe = ffmpeg.probe(input_file_path)
        except ffmpeg.Error as error:
            # Log the error for debugging and re-raise it
            print(f"ffprobe stderr: {error.stderr.decode('utf-8')}")
            raise error

        # Calculate the time offset for the thumbnail (middle of the video duration)
        duration = float(probe["format"]["duration"])
        time_offset = duration / 2

        # Get the video width from the metadata
        video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
        width = int(video_stream["width"])

        # Generate the thumbnail using ffmpeg at the calculated time offset
        try:
            (
                ffmpeg.input(input_file_path, ss=time_offset)
                .filter("scale", width, -1)
                .output(thumbnail_file_path, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as error:
            # Log the error for debugging and re-raise it
            print(f"ffmpeg stderr: {error.stderr.decode('utf-8')}")
            raise error

        # Open the thumbnail file, create a Django ContentFile from it and save to the model
        with open(thumbnail_file_path, "rb") as file:
            content_file = ContentFile(file.read(), name=thumbnail_file_path)
            self.thumbnail.save(content_file.name, content_file)
            self.save()

        # Remove the local thumbnail file after it has been saved to the model
        os.remove(thumbnail_file_path)

        # Return the saved thumbnail
        return self.thumbnail.url
