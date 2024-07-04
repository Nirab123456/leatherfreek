from django.apps import AppConfig


class LeatherWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leather_web'

    def ready(self):
        import leather_web.signals