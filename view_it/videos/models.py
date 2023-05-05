import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .validators import validate_video_file_type, validate_video_thumbnail_file_type

User = get_user_model()


class Videos(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"

    STATUS_CHOICES = (
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
    )

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
        upload_to="videos/%Y/%m/%d/%H/",
        null=False,
        blank=False,
        validators=[validate_video_file_type],
        help_text=_("Required. Supported file types are: .mp4, .webm, and .ogv"),
    )

    thumbnail = models.FileField(
        _("Thumbnail File Path"),
        upload_to="thumbnails/%Y/%m/%d/%H/",
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
