
"""
Serlizers for the listing model
"""


from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    # override title to accept at least two chars
    title = serializers.CharField(min_length=2)
    owner = serializers.HiddenField(
                            default=serializers.CurrentUserDefault())
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Listing
        
        
        fields = ('id', 
                  'title', 
                  'description',
                  'price',
                  'image',
                  'category',
                  'owner',
                  'creation_date',
                  'modification_date',
                  'slug'
        )

    def create(self, validated_data):
        # set the owner
        self.owner = self.context['request'].user
        return super().create(validated_data)

  

