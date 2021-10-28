
"""
Utilities and helper function.
"""

import os
import glob
from datetime import datetime
import random
from pathlib import Path
import shutil
import json

# django and project stuff
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.conf import settings

from .models import Listing, Category   


# configuration loaders
def load_configurations(file='fair/configurations.json', block="dummy_listings"):
    """
        Load the configurations from a json file
    """
    with open(file) as json_file:
        configurations = json.load(json_file)
    
    return configurations["dummy_listings"]

### Dummy listings related helpers


def create_listings(request, configurations_block="dummy_listings"):
    """
    Create dummy listings by random sampling from a dataset.

    :param: request is the user request
    :configuration_block: a dictionary of configurations to create the random listings
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
            files_ = glob.glob(f'{data_path}{folder}{os.sep}{extension}')
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
            image_file_name = f'images{os.sep}{listing.id}{os.path.splitext(file)[-1]}'                                 
            listing.image.name = image_file_name
            listing.save()

             # copy the file to MEDIA_ROOT/images
            listing_images_path = settings.MEDIA_ROOT
            print(file, f'{listing_images_path}{image_file_name}')
            shutil.copyfile(file, f'{listing_images_path}{image_file_name}')

    return HttpResponseRedirect(reverse('home'))