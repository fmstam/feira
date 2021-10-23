from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .auth import AuthenticationManager

class FairConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fair'

    def ready(self):
        # after migration where we have created the groups assing permissions
        post_migrate.connect(AuthenticationManager.initialize, sender=self)