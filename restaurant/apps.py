from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    name = 'restaurant'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import restaurant.signals
        import API.celery
