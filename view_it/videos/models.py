from django.db import models

from view_it.users.models import User


class Videos(models.model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_title = models.CharField(max_length=200)
    video_description = models.TextField()
    file = models.FileField(upload_to="videos/%Y/%m/%d/%H/")
    published_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_title
