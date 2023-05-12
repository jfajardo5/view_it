import pytest

from view_it.utils.videos_utils import create_test_image, create_test_video
from view_it.videos.tests.factories import VideoFactory

pytestmark = pytest.mark.django_db


class TestSearchSignals:
    def test_add_video_to_search_index_is_being_called(self, tmp_path, mocker):
        # Try using the full path to the delay function
        mock_delay = mocker.patch("view_it.search.tasks.add_video_to_search_index.delay")

        # Mock transaction.on_commit to immediately execute the provided function
        mocker.patch("django.db.transaction.on_commit", side_effect=lambda func: func())

        # Create a video
        video = VideoFactory.build(
            file=create_test_video(tmp_path, "mp4"),
            thumbnail=create_test_image(tmp_path, "png"),
        )

        # Save user before saving video
        video.user.save()

        # Save video
        video.save()

        mock_delay.assert_called_once_with(video_id=video.id)

    def test_add_video_to_search_index_is_not_being_called_on_private_videos(self, tmp_path, mocker):
        # Try using the full path to the delay function
        mock_delay = mocker.patch("view_it.search.tasks.add_video_to_search_index.delay")

        # Mock transaction.on_commit to immediately execute the provided function
        mocker.patch("django.db.transaction.on_commit", side_effect=lambda func: func())

        # Create a video
        video = VideoFactory.build(
            file=create_test_video(tmp_path, "mp4"),
            thumbnail=create_test_image(tmp_path, "png"),
            status="private",
        )

        # Save user before saving video
        video.user.save()

        # Save video
        video.save()

        mock_delay.assert_not_called()
