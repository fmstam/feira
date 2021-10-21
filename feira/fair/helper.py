
"""
A helper file to fill the database and create dummy records
"""

import os
import glob
from datetime import datetime
import random
from pathlib import Path
import shutil


from django.http import HttpResponseRedirect
from django.urls.base import reverse
from .models import Listing, Category   


# setup 
data_path =  "/home/ftam/Downloads/clothing-dataset-small-master/dataset"
data_folders = {'Dress': 'dress', 'Shirt': 'shirt', 'toptee':'toptee'} # categories in the listing
n_listings =  5
prices =  range(5, 120, 5)
unique =  True
extensions =  ['*.jpeg', '*.jpg', '*.png']


def create_listings(request):
    for cate, folder in data_folders.items():
        files = []
        for extension in extensions:
            files_ = glob.glob(f'{data_path}{os.sep}{folder}{os.sep}{extension}')
            files.extend(files_)
        category = Category.objects.get(name=cate)

        for file in random.sample(files, k=n_listings):
            listing = Listing(title=cate, 
                              price=random.choice(prices),
                              creation_date=datetime.now(),
                              modification_date=datetime.now(),
                              owner=request.user,
                              category=category
                              )
            
            
            listing.save()

            # store the image
            image_file_name = f'listings_images{os.sep}{listing.id}{os.path.splitext(file)[-1]}'                                 
            listing.image.name = image_file_name
            listing.save()

             # copy the file to MEDIA_ROOT/listing_images
            listing_images_path = '/home/ftam/Dropbox/webdev/django/feira/feira/media/'
            shutil.copyfile(file, f'{listing_images_path}{os.sep}{image_file_name}')

    return HttpResponseRedirect(reverse('home'))