from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import VideoUploadForm
from .models import Videos


class HomePageView(SuccessMessageMixin, TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["public_videos"] = Videos.objects.filter(status="public").order_by("-uploaded_timestamp")[:20]

        return context


home_page_view = HomePageView.as_view()


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
    slug_field = "url_slug"
    slug_url_kwarg = "url_slug"
    fields = ["title", "description", "thumbnail", "status"]
    template_name = "videos/update_video.html"
    success_message = _("Information successfully updated!")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return reverse("videos:detail", kwargs={"url_slug": self.object.url_slug})

    def get_object(self):
        return Videos.objects.filter(url_slug=self.kwargs["url_slug"], user=self.request.user.id).first()


video_update_view = VideoUpdateView.as_view()
