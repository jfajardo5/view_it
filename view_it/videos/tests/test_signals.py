import pytest

from view_it.utils.videos_utils import create_test_image, create_test_video
from view_it.videos.tests.factories import VideoFactory

pytestmark = pytest.mark.django_db


class TestVideoCreatedSignal:
    def test_generate_thumbnail_was_called(self, tmp_path, mocker):
        # Try using the full path to the delay function
        mock_delay = mocker.patch("view_it.videos.tasks.generate_thumbnail.delay")

        # Mock transaction.on_commit to immediately execute the provided function
        mocker.patch("django.db.transaction.on_commit", side_effect=lambda func: func())

        # Create a video
        video = VideoFactory.build(file=create_test_video(tmp_path, "mp4"))

        # Save user before saving video
        video.user.save()

        # Save video
        video.save()

        mock_delay.assert_called_once_with(video.id, video.file.url)

    def test_generate_thumbnail_is_only_called_if_video_has_no_thumbnail(self, tmp_path, mocker):
        # Try using the full path to the delay function
        mock_delay = mocker.patch("view_it.videos.tasks.generate_thumbnail.delay")

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

        mock_delay.not_called(video.id, video.file.url)

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

        mock_delay.assert_called_once_with(video.id)

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
