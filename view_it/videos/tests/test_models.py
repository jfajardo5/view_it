import pytest

from .factories import VideoFactory


@pytest.fixture
def video(db):
    return VideoFactory()


def test_video_get_absolute_url(video: VideoFactory):
    assert video.get_absolute_url() == f"/video/{video.url_slug}/"
