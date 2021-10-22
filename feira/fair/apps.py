from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .auth import AuthenticationManager

class FairConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fair'

    def ready(self):
        post_migrate.connect(AuthenticationManager.assing_permissions(AuthenticationManager.group_permissions))