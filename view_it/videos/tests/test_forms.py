"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _
from factory import Faker

from view_it.users.tests.factories import UserFactory
from view_it.utils.test_utils import create_test_image, create_test_video
from view_it.videos.forms import VideoUploadForm


@pytest.mark.django_db
class TestVideoUploadForm:
    def test_video_can_be_uploaded(self, tmp_path):
        # create a user using UserFactory
        user = UserFactory()

        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # assert that the form is valid
        assert form.is_valid()

    def test_title_is_required(self, tmp_path):
        # create a user using UserFactory
        user = UserFactory()

        # create an instance of the form with no title
        form = VideoUploadForm(
            {
                "user": user.id,
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # assert that the form is not valid
        assert not form.is_valid()
        # assert that the title field has an error message
        assert "title" in form.errors
        assert str(form.errors["title"][0]) == str(_("This field is required."))

    def test_file_is_required(self, tmp_path):
        # create a user using UserFactory
        user = UserFactory()

        # create an instance of the form with no file
        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # assert that the form is not valid
        assert not form.is_valid()
        # assert that the file field has an error message
        assert "file" in form.errors
        assert str(form.errors["file"][0]) == str(_("This field is required."))

    def test_video_form_with_invalid_file_type_fails(self, tmp_path):
        # Create a new user using the UserFactory
        user = UserFactory()

        # Create a VideoUploadForm with a file of invalid type (text/plain)
        # and a valid thumbnail
        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "avi"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # Assert that the form is not valid
        assert not form.is_valid()

        # Assert that the "file" field has an error
        assert "file" in form.errors

    def test_video_form_with_invalid_thumbnail_type_fails(self, tmp_path):
        # Create a new user using the UserFactory
        user = UserFactory()

        # Create a VideoUploadForm with a valid file
        # and a thumbnail of invalid type (text/plain)
        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "bmp"),
            },
        )

        # Assert that the form is not valid
        assert not form.is_valid()

        # Assert that the "thumbnail" field has an error
        assert "thumbnail" in form.errors

    def test_description_is_optional(self, tmp_path):
        # create a user using UserFactory
        user = UserFactory()

        # create an instance of the form with no description
        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "status": "public",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # assert that the form is valid
        assert form.is_valid()

    def test_status_is_required(self, tmp_path):
        # create a user using UserFactory
        user = UserFactory()

        # create an instance of the form with no status
        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # assert that the form is not valid
        assert not form.is_valid()
        # assert that the status field has an error message
        assert "status" in form.errors
        assert str(form.errors["status"][0]) == str(_("This field is required."))

    def test_invalid_status_choice_fails(self, tmp_path):
        # create a user using UserFactory
        user = UserFactory()

        # create an instance of the form with an invalid status choice
        form = VideoUploadForm(
            {
                "user": user.id,
                "title": Faker("sentence", nb_words=5),
                "description": Faker("paragraph", nb_sentences=5),
                "status": "invalid_choice",
            },
            files={
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
        )

        # assert that the form is not valid
        assert not form.is_valid()
        # assert that the status field has an error message
        assert "status" in form.errors
        assert str(form.errors["status"][0]) == str(
            _("Select a valid choice. invalid_choice is not one of the available choices.")
        )
