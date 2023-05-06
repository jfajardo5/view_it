import pytest
from django.urls import resolve, reverse

from view_it.videos.tests.factories import VideoFactory


@pytest.mark.django_db
class VideoViewsTests:
    def test_detail():
        video = VideoFactory()
        assert reverse("videos:detail", kwargs={"url_slug": video.url_slug}) == f"/video/{video.url_slug}/"
        assert resolve(f"/video/{video.url_slug}/").view_name == "videos:detail"
