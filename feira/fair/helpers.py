
"""
Utilities and helper function.
"""

import os
import glob
from datetime import datetime
import random
from pathlib import Path
import shutil

# django and project stuff
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.conf import settings

from .models import Listing, Category   

import json


# configuration loaders
def load_configurations(file='configurations.json', block="description"):
    """
        Load the configurations from a json file
    """
    with open(file) as json_file:
            configurations = json.load(block)
    
    return configurations

### Dummy listings related helpers


def create_listings(request, configurations_block="dummy_listings"):
    """
    Create dummy listings.
    """

    # setup 
    configurations = load_configurations(block=configurations_block)
    data_path =  configurations['data_path']
    data_folders = configurations['data_folders']
    n_listings =  configurations['n_listings']
    start, end, step = configurations['prices']
    prices =  range(start, end, step)
    unique =  configurations['unique']
    extensions =  configurations['extensions'] #['*.jpeg', '*.jpg', '*.png']

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
            listing_images_path = settings.MEDIA_ROOT
            shutil.copyfile(file, f'{listing_images_path}{os.sep}{image_file_name}')

    return HttpResponseRedirect(reverse('home'))