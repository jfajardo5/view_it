import pytest
from django.urls import reverse

from view_it.users.tests.factories import UserFactory
from view_it.utils.test_utils import create_test_image, create_test_video
from view_it.videos.models import Videos


@pytest.mark.django_db
class TestVideoCreateView:
    """
    Test cases for the `VideoCreateView` view.
    """

    def test_video_create_view_loads(self, client):
        """
        Test that the `VideoCreateView` loads successfully when accessed by a logged-in user.
        """

        # Generate the URL for the `VideoCreateView` view.
        url = reverse("videos:upload")

        # Create a user instance using the `UserFactory`.
        user = UserFactory()

        # Login the client with the created user.
        client.force_login(user)

        # Send a GET request to the URL and check that the response status code is 200.
        response = client.get(url)
        assert response.status_code == 200

    def test_video_create_view_cannot_be_accessed_by_a_guest_user(self, client):
        """
        Test that the `VideoCreateView` cannot be accessed by a guest user and
        redirects to the login page.
        """

        # Generate the URL for the `VideoCreateView` view.
        url = reverse("videos:upload")

        # Send a GET request to the URL and check that the response status code is 302.
        response = client.get(url)
        assert response.status_code == 302

    def test_video_create_view_creates_video(self, client, tmp_path):
        """
        Test that the `VideoCreateView` creates a video instance when the form is submitted with valid data.
        """

        # Generate the URL for the `VideoCreateView` view.
        url = reverse("videos:upload")

        # Create a user instance using the `UserFactory`.
        user = UserFactory()

        # Login the client with the created user.
        client.force_login(user)

        # Submit a POST request to the URL with valid form data.
        response = client.post(
            url,
            {
                "title": "Test video title",
                "description": "Test video description",
                "status": "public",
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
            follow=True,
        )

        # Check that the response status code is 200 and the video is created in the database.
        assert response.status_code == 200
        assert Videos.objects.count() == 1
        video = Videos.objects.first()
        assert video.title == "Test video title"
        assert video.description == "Test video description"
        assert video.status == "public"
        assert video.user == user

    def test_video_create_view_requires_login(self, client, tmp_path):
        """
        Test that the `VideoCreateView` view requires the user to be logged in to create a video instance.
        """

        # Generate the URL for the `VideoCreateView` view.
        url = reverse("videos:upload")

        # Submit a POST request to the URL with valid form data.
        response = client.post(
            url,
            {
                "title": "Test video title",
                "description": "Test video description",
                "status": "public",
                "file": create_test_video(tmp_path, "mp4"),
                "thumbnail": create_test_image(tmp_path, "png"),
            },
            follow=True,
        )

        # Check that the response status code is 200 and that the user is redirected to the login page.
        assert response.status_code == 200
        assert response.redirect_chain == [("/accounts/login/?next=" + url, 302)]
        assert Videos.objects.count() == 0
