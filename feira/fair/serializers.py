
"""
Serlizers for the listing model
"""


from django.template.defaultfilters import default
from rest_framework import serializers
from .models import Listing
from .ML import TaskResult

 
class TaskSerializer(serializers.Serializer):
    task_name = serializers.CharField(min_length=2)
    task_id   = serializers.SlugField(allow_blank=True)
    action    = serializers.ChoiceField(choices=('START', 'STOP'))  

    
class TaskResultsSerializer(serializers.ModelSerializer):
    """
    Serializer for ML Celery tasks results 
    """
    task_id = serializers.CharField()
    task_state = serializers.CharField()
    current_results = serializers.DictField()

    def create(self, validated_data):
        return TaskResult(**validated_data)



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

  

