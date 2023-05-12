from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "view_it.search"
    verbose_name = _("Search")

    def ready(self):
        try:
            import view_it.search.signals  # noqa
        except ImportError:
            pass
