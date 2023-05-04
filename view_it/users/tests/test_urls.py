from django.urls import resolve, reverse

from view_it.users.models import User


def test_detail(user: User):
    assert reverse("users:detail", kwargs={"username": user.username}) == f"/@{user.username}/"
    assert resolve(f"/@{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/@~update/"
    assert resolve("/@~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/@~redirect/"
    assert resolve("/@~redirect/").view_name == "users:redirect"
