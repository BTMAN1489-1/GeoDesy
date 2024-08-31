from django.apps import AppConfig
from geodesy import settings

__all__ = ("MainAppConfig",)


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Для сотрудников'
    name = 'main_app'

    def ready(self):
        super().ready()
        if settings.DEBUG:
            import main_app.schema


