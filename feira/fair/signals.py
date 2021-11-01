""" signals handlers """

## permissions imports
from typing import List
from django.core import serializers
from django.db.models import ProtectedError
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save


# models and fields
from .models import ActivityLog, DeletedData, Listing
from django.contrib.auth.models import User
import django.utils.timezone as timezone


## shortcuts

def create_activity(user, action, at=timezone.now()):
    ActivityLog.objects.create(by=user, 
                                action=action,
                                at=timezone.now())

## 1. Signals on Listing model

# protect uneditable fields
@receiver(pre_save, sender=Listing)
def pre_save_listing_protection(sender, 
                                instance,
                                **kwargs):
    try:
        object = sender.objects.get(pk=instance.pk)
    except:
        return # all new, just ignore
    else: # check for any unacceptable modification
        if instance.owner != object.owner: # listing owner can be changed
            action = f'{instance.owner} tries to change owner from {object.owner} to {instance.owner}'
            create_activity(instance.owner, action) # record the activity
            raise ProtectedError('`user` can be modified.')
        if instance.creation_date != object.creation_date: # creation date is fixed
            action = f'{instance.owner} tries to change owner from {object.creation_date} to {instance.creation_date}'
            create_activity(instance.owner, action) # record the activity
            raise ProtectedError('`creation time stamp` can be modified.')
        if instance.slug != object.slug: # slug is fixed
            action = f'{instance.owner} tries to change owner from {object.slug} to {instance.slug}'
            create_activity(instance.owner, action) # record the activity
            raise ProtectedError('`identifier` can be modified.')
    
    

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
    create_activity(user, action) # record the activity

    
### archive listing 
@receiver(post_delete, sender=Listing)
def archive_Listing(sender, instance, **kwargs):
    data = serializers.serialize('json', [instance])
    DeletedData.objects.create(
        model_name='Listing',
        instance_id=instance.id,
        data=data

    )


# 2. Signals on X model ...