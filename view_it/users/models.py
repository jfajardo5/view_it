from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, FileField, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for View It.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    name_validator = RegexValidator(
        regex=r"^[A-Za-z]{2,30}$"  # 2 to 30 characters in length. Alphabetic characters only.
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
        validators=[name_validator],
        help_text="Required. 30 characters or fewer. Alphabetical characters only.",
        max_length=30,
    )

    last_name = CharField(
        _("Last Name"),
        null=True,
        validators=[name_validator],
        help_text="Required. 30 characters or fewer. Alphabetical characters only.",
        max_length=30,
    )

    avatar = FileField(_("Avatar"), upload_to="avatars/%Y/%m/%d/%H/", blank=True)

    channel_description = TextField(_("Channel Description"), blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
