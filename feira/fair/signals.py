## permissions imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from .auth import AuthTools # our manager




# models and fields
from .models import ActivityLog, Listing
from django.contrib.auth.models import User
import django.utils.timezone as timezone


# On Listing model
# Set permission post-saving
@receiver(post_save, sender=Listing)
def set_listing_premissions(sender, instance, **kwargs):
    user = User.objects.get(id=instance.owner.id)
    assign_perm(AuthTools.CHANGE_LISTING, user) # on the model
    assign_perm(AuthTools.CHANGE_LISTING, user, instance) # on the instance

# Activity log
# this can be replaced by django-simple-history or the like
# https://django-simple-history.readthedocs.io/en/latest/

@receiver(post_save, sender=Listing)
def post_save_listing_activity(sender, 
                               instance,
                               **kwargs):
    """
    Log when a listing is modified/created.
    This is not the right way, and should be replaced by a framework
    """
    user = User.objects.get(id=instance.owner.id)
    action = f'{user.username} with id {user.id} changed listing with id {instance.id}'
    ActivityLog.objects.create(by=user, 
                                action=action,
                                at=timezone.now())
    

