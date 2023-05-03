"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _

from view_it.users.forms import UserAdminCreationForm, UserSignupForm
from view_it.users.models import User

pytestmark = pytest.mark.django_db


class TestUserSignupForm:
    """
    Test class for all tests related to the UserSignupForm
    """

    def test_regular_user_is_able_to_sign_up(self):
        form = UserSignupForm(
            {
                "email": "test@test.com",
                "username": "testguy",
                "first_name": "Test",
                "last_name": "Guy",
                "password1": "u6vQcD8SEWdLbAL",
                "password2": "u6vQcD8SEWdLbAL",
            }
        )
        assert form.is_valid()

    def test_regular_user_cannot_sign_up_with_an_existing_email(self, user: User):
        form = UserSignupForm(
            {
                "email": user.email,
                "username": "testguy",
                "first_name": "Test",
                "last_name": "Guy",
                "password1": "u6vQcD8SEWdLbAL",
                "password2": "u6vQcD8SEWdLbAL",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors

    def test_regular_user_cannot_sign_up_with_an_existing_username(self, user: User):
        form = UserSignupForm(
            {
                "email": "test@test.com",
                "username": user.username,
                "first_name": "Test",
                "last_name": "Guy",
                "password1": "u6vQcD8SEWdLbAL",
                "password2": "u6vQcD8SEWdLbAL",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors

    def test_regular_user_cannot_sign_up_without_first_name(self):
        form = UserSignupForm(
            {
                "email": "test@test.com",
                "username": "testguy",
                "first_name": "",
                "last_name": "Guy",
                "password1": "u6vQcD8SEWdLbAL",
                "password2": "u6vQcD8SEWdLbAL",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "first_name" in form.errors

    def test_regular_user_cannot_sign_up_without_last_name(self):
        form = UserSignupForm(
            {
                "email": "test@test.com",
                "username": "testguy",
                "first_name": "Test",
                "last_name": "",
                "password1": "u6vQcD8SEWdLbAL",
                "password2": "u6vQcD8SEWdLbAL",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "last_name" in form.errors

    def test_regular_user_cannot_sign_up_without_matching_passwords(self):
        form = UserSignupForm(
            {
                "email": "test@test.com",
                "username": "testguy",
                "first_name": "Test",
                "last_name": "Guy",
                "password1": "u6vQcD8SEWdLbALzsd",
                "password2": "u6vQcD8SEWdLbAL",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors

    def test_regular_user_cannot_sign_up_without_a_password(self):
        form = UserSignupForm(
            {
                "email": "test@test.com",
                "username": "testguy",
                "first_name": "Test",
                "last_name": "Guy",
                "password1": "",
                "password2": "",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert "password1" in form.errors
        assert "password2" in form.errors


class TestUserAdminCreationForm:
    """
    Test class for all tests related to the UserAdminCreationForm
    """

    def test_username_validation_error_msg(self, user: User):
        """
        Tests UserAdminCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserAdminCreationForm(
            {
                "username": user.username,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == _("This username has already been taken.")
