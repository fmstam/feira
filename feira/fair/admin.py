from django.contrib import admin
from fair.models import *

# Register your models here.
admin.site.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'description', 'image', 'slug']

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

admin.site.register(Similarity)
class SimilarityAdmin(admin.ModelAdmin):
    list_display = ['score', 'listing_1', 'listing_2']


admin.site.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'by', 'at']