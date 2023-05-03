from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_name(value):
    """
    Validator for name fields.
    """
    return RegexValidator(regex=r"^[A-Za-z]{2,30}$")  # 2 to 30 characters in length. Alphabetic characters only.


def validate_unique_email(value):
    """
    Validator that verifies if email is unique in the database.
    """
    try:
        get_user_model().objects.get(email=value)
    except get_user_model().DoesNotExist:
        return

    raise ValidationError(
        _("An account has already registered with %(value)s. Try resetting your password."),
        params={"value": value},
    )
