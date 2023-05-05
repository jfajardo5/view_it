from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, FileField, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .validators import validate_avatar_file_type, validate_name, validate_unique_email


class User(AbstractUser):
    """
    Default custom user model for View It.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)

    email = EmailField(
        _("email address"),
        blank=True,
        unique=True,
        validators=[validate_unique_email],
        help_text=_("Required. Must be an unique and valid email address."),
    )

    username = CharField(
        _("Username"),
        max_length=30,
        unique=True,
        help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )

    first_name = CharField(
        _("First Name"),
        null=True,
        validators=[validate_name],
        help_text="Required. 30 characters or fewer. Alphabetical characters only.",
        max_length=30,
    )

    last_name = CharField(
        _("Last Name"),
        null=True,
        validators=[validate_name],
        help_text="Required. 30 characters or fewer. Alphabetical characters only.",
        max_length=30,
    )

    avatar = FileField(
        _("Avatar"),
        upload_to="avatars/%Y/%m/%d/%H/",
        blank=True,
        validators=[validate_avatar_file_type],
        help_text="Supported file types are: .jpg, .jpeg, .png, and .gif",
    )

    channel_description = TextField(_("Channel Description"), blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
