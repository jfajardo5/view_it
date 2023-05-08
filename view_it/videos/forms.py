from django import forms

from view_it.videos.models import Videos

from .tasks import create_thumbnail_from_video


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ["title", "description", "file", "thumbnail", "status"]

    def save(self, commit=True):
        video = super().save(commit=commit)
        if commit:
            if not video.thumbnail:
                create_thumbnail_from_video.delay(video.file.url, video.id)

        return video
