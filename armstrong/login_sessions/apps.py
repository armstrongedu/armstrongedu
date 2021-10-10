from django.apps import AppConfig


class LoginSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login_sessions'

    def ready(self):
        from . import signals
