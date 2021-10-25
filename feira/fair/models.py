# models
from typing import List
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.core import serializers

# urls
from django.urls import reverse

# auth imports
from django.contrib.auth.models import User

from fair.encryptions import EncryptedTextField



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
                                null=True)   # category 

    # other possible fields 
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
    

## Activity log models

class ActivityLog(models.Model):
    by = models.ForeignKey(User, 
                            null=True,
                            on_delete=models.SET_NULL) # let it there if the user gets deleted
    action = EncryptedTextField(max_length=256)
    at = models.DateTimeField()

    class Meta:
        ordering = ['-at']
        verbose_name_plural = 'Activities'


class DeletedData(models.Model):
    model_name  = models.CharField(max_length=200) #
    instance_id = models.IntegerField()
    data        = models.TextField()

    @classmethod
    def restore_deleted(cls, instance_id):
        """
        Restore a deleted object.
        To see how an object is handeled see post_delete receivers in signal.py
        """
        deleted =  cls.objects.get(model_name = 'Listing', instance_id=instance_id)
        for instance in serializers.deserialize('json', deleted.data):
            instance.save()
            deleted.delete()

    class Meta:
        verbose_name_plural = 'DeletedData'

    


## ML-related models/tables
class Similarity(models.Model):
    """
    Represents the similarity matrix between two listings:
    - listing_1: first listing
    - listing_1: second listing

    NOTE: A better way would be a sparse data structure which I will do in the second sprint.
    For now allowing the fields to be blank will make things ok.
    """
    score = models.FloatField(blank=True, null=True)
    listing_1 = models.ForeignKey(Listing, on_delete=CASCADE, related_name='related_listing_1')
    listing_2 = models.ForeignKey(Listing, on_delete=CASCADE, related_name='related_listing_2')

    class Meta:
        verbose_name_plural = 'Similarities'
    
