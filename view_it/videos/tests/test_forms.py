"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _
from factory import Faker

from view_it.utils.test_utils import create_test_image, create_test_video
from view_it.videos.forms import VideoUploadForm


@pytest.mark.django_db
class TestVideoUploadForm:
    def test_form_can_be_valid_with_mp4_video(self, tmp_path):
        """
        Test that the form is valid when using an MP4 video file
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert form.is_valid()

    def test_form_can_be_validated_with_ogg_video(self, tmp_path):
        """
        Test that the form is valid when using an OGG video file
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "ogg"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert form.is_valid()

    def test_form_can_be_validated_with_webm_video(self, tmp_path):
        """
        Test that the form is valid when using a WebM video file
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "webm"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert form.is_valid()

    def test_form_cannot_be_validated_with_unsupported_video_file_type(self, tmp_path):
        """
        Test that the form is not valid when using an unsupported video file type
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "avi"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert not form.is_valid()

    def test_title_is_required(self, tmp_path):
        """
        Test that the title field is required
        """
        form = VideoUploadForm(
            {
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert not form.is_valid()
        assert "title" in form.errors
        assert str(form.errors["title"][0]) == str(_("This field is required."))

    def test_file_is_required(self, tmp_path):
        """
        Test that the form is invalid when the file is missing.
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert not form.is_valid()
        assert "file" in form.errors
        assert str(form.errors["file"][0]) == str(_("This field is required."))

    def test_video_form_with_invalid_file_type_fails(self, tmp_path):
        """
        Test that the form is invalid when the video file type is not supported.
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "avi"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert not form.is_valid()
        assert "file" in form.errors

    def test_video_form_with_invalid_thumbnail_type_fails(self, tmp_path):
        """
        Test that the form is invalid when the thumbnail file type is not supported.
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "bmp"),
            },
        )

        assert not form.is_valid()
        assert "thumbnail" in form.errors

    def test_description_is_optional(self, tmp_path):
        """
        Test that the form is valid when the description field is not provided.
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert form.is_valid()

    def test_status_is_required(self, tmp_path):
        """
        Test that the form is invalid when the status field is missing.
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert not form.is_valid()
        assert "status" in form.errors
        assert str(form.errors["status"][0]) == str(_("This field is required."))

    def test_invalid_status_choice_fails(self, tmp_path):
        """
        Tests that the form is not valid when an invalid status choice is provided.
        """
        form = VideoUploadForm(
            {
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "invalid_choice",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        assert not form.is_valid()
        assert "status" in form.errors
        assert str(form.errors["status"][0]) == str(
            _("Select a valid choice. invalid_choice is not one of the available choices.")
        )
