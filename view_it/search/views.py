from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView

from view_it.videos.models import Videos


class HomePageView(SuccessMessageMixin, TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["public_videos"] = (
            Videos.objects.filter(status="public").order_by("-uploaded_timestamp").select_related("user")[:20]
        )

        return context


home_page_view = HomePageView.as_view()


class SearchView(SuccessMessageMixin, TemplateView):
    template_name = "search/videos.html"


search_view = SearchView.as_view()
