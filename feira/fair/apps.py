from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .auth import AuthTools

class FairConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fair'

    def ready(self):
        
        # after migration and group creation, assign permissions
        # post_migrate.connect(AuthTools.initialize, sender=self)

        # load signals 
        import fair.signals