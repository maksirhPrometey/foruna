from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.content'
    verbose_name = 'Контент'

    def ready(self) -> None:
        from src.content import signals  # noqa: F401
