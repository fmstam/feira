from operator import mod
from typing import Iterable, Optional
from unicodedata import category, name
from django.db import models

from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils import timezone




class Category(models.Model):
        """
        a Typical category class
        """

        name = models.CharField(max_length=64)
        slug = models.SlugField(max_length=64, 
                                unique=True,
                                default='name')


        class Meta:
            ordering = ['name']
            verbose_name_plural = 'categories'

        def get_absolute_url(self):
            return reverse('fair:category_listings', args=[self.slug])
        def __str__(self) -> str:
            return self.name


class Listing(models.Model):
    """
    A typical listing in the marketplace.
    It has title, creation_date, modification_date, description, ...
    """

    title = models.CharField(max_length=256)
    creation_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(editable=False)
    description = models.TextField(max_length=1024,
                                    blank=True)
    price = models.DecimalField(blank=False,
                                decimal_places=2,
                                max_digits=6,
                                default=0)
                                  
    image = models.ImageField(upload_to='listings_images',
                             blank=True, # not required in the form
                             null=True) # can be NULL in the db
    owner = models.ForeignKey(User, 
                                on_delete=CASCADE,
                                related_name="user_listings") # user id
    category = models.ForeignKey(Category, 
                                on_delete=CASCADE,
                                related_name="categories",
                                null=False)   # category 

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
        constraints = [models.CheckConstraint(check=models.Q(price__gte='0'), name='price_non_negative'),]

    def save(self, *args, **kwargs):
        """
        Override the save method to setup created and modified fields
        """
        if not self.id:
            self.creation_date = timezone.now()
        self.modification_date = timezone.now()
    
        return super(Listing, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('fair:category_listings', args=[self.slug])
    
    

    



    
