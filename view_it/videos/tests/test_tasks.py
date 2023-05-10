import pytest

from view_it.utils.videos_utils import create_test_video
from view_it.videos.models import Videos
from view_it.videos.tasks import generate_thumbnail
from view_it.videos.tests.factories import VideoFactory

pytestmark = pytest.mark.django_db


class TestGenerateThumbnail:
    """
    This class contains test cases for the generate_thumbnail function in view_it.videos.tasks.
    """

    def test_generate_thumbnail_executes_successfully(self, settings, mocker, tmp_path):
        # Mock the settings object to use the pytest tmp_path as the APPS_DIR and MEDIA_ROOT directories.
        mocker.patch.object(settings, "APPS_DIR", str(tmp_path))
        mocker.patch.object(settings, "MEDIA_ROOT", f"{str(tmp_path)}/media")

        # Create a video object with a mock video file.
        video = VideoFactory.build(file=create_test_video(tmp_path, "mp4"))

        # Save the user associated with the video object.
        video.user.save()

        # Save the video object.
        video.save()

        assert not video.thumbnail

        # Call the generate_thumbnail function for the video object.
        result = generate_thumbnail(video_id=video.id, video_url=video.file.url)

        # Get the video object from the database to check if the thumbnail was generated.
        with_thumbnail = Videos.objects.get(id=video.id)

        # Check if the generate_thumbnail function returned a valid result and if the video object now has a thumbnail.
        assert result
        assert with_thumbnail.thumbnail
