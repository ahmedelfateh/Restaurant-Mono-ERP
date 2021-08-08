from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestaurantsConfig(AppConfig):
    name = "app.restaurants"
    verbose_name = _("Restaurants")

    def ready(self):
        try:
            import app.restaurants.signals  # noqa F401
        except ImportError:
            pass
