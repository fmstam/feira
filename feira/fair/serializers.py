
"""
Serlizers for the listing model
"""


from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    # override title to accept at least two chars
    title = serializers.CharField(min_length=2)
    
    class Meta:
        model = Listing
        fields = ('id', 
                  'title', 
                  'creation_date', 
                  'modification_date',
                  'description',
                  'price',
                  'image',
                  'owner',
                  'category',
                  'slug'
        )

  

