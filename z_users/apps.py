from django.apps import AppConfig


class ZUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'z_users'

    def ready(self):
        from . import signals