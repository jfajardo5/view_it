from django.db import models
from django.utils.translation import gettext_lazy as _

from view_it.users.models import User


class Videos(models.model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_title = models.CharField(_("Video Title"), max_length=200)
    video_description = models.TextField(_("Video Description"))
    file = models.FileField(_("Video File Path"), upload_to="videos/%Y/%m/%d/%H/")
    uploaded_timestamp = models.DateTimeField(_("Video Upload Timestamp"), auto_now_add=True)

    def __str__(self) -> str:
        return self.video_title
