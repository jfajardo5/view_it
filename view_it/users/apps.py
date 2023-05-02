from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "view_it.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import view_it.users.signals  # noqa: F401
        except ImportError:
            pass
