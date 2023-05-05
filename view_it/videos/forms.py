from django import forms

from view_it.videos.models import Videos


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ["title", "description", "file", "thumbnail", "status"]
