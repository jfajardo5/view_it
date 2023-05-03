from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from view_it.users.validators import validate_name, validate_unique_email

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    email = forms.EmailField(
        label=_("Email"),
        validators=[validate_unique_email],
        widget=forms.TextInput(attrs={"placeholder": _("Email"), "autocomplete": "email"}),
    )

    first_name = forms.CharField(
        label=_("First Name"),
        min_length=2,
        max_length=30,
        validators=[validate_name],
        widget=forms.TextInput(attrs={"placeholder": _("First Name"), "autocomplete": "first_name"}),
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        min_length=2,
        max_length=30,
        validators=[validate_name],
        widget=forms.TextInput(attrs={"placeholder": _("Last Name"), "autocomplete": "last_name"}),
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
