from operator import mod
from typing import Iterable, Optional
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Listing(models.Model):
    """
    A typical listing in the marketplace.
    It has title, creation_date, modification_date, description, ...
    """

    title = models.CharField(max_length=256)
    creation_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField()
    description = models.TextField(max_length=1024,
                                  blank=True)
    image = models.ImageField(upload_to='listings_images',
                             blank=True, # not required in the form
                             null=True) # can be NULL in the db

    # still_available = models.BooleanField()                                 
    # accept_offers = models.BooleanField()


    # to create unique URL for lists
    slug = models.SlugField(max_length=128,
                            default='title',
                            unique_for_date='creation_date',
                            db_index=True
                            )


    class Meta:
        ordering = ['-modification_date']
        index_together = (('id', 'slug'))

    def save(self, *args, **kwargs):
        """
        Override the save method to setup created and modified fields
        """
        if not self.id:
            self.creation_date = timezone.now()
        self.modification_date = timezone.now()
    
        return super(Listing, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('fair:listings', args=[self.slug])
    
    


    
