from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import VideoUploadForm
from .models import Videos


class VideoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Videos
    form_class = VideoUploadForm
    template_name = "videos/upload_video.html"
    success_message = _("Video successfully uploaded!")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


video_upload_view = VideoCreateView.as_view()


class VideoDetailView(DetailView):
    model = Videos
    slug_field = "url_slug"
    slug_url_kwarg = "url_slug"
    template_name = "videos/view_video.html"


video_detail_view = VideoDetailView.as_view()


class VideoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Videos
    fields = ["video_title", "video_description", "thumbnail", "status"]
    success_message = _("Information successfully updated!")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()


video_update_view = VideoUpdateView.as_view()
