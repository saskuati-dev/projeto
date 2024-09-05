from django.apps import AppConfig


class AppSiadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_siad'

    def ready(self):
            import app_siad.signals  