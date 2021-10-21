
"""
A helper file to fill the database and create dummy records
"""

import glob
from datetime import datetime
import random
from typing import List

from django.core.files import File

from .models import Listing, Category   




# setup 
data_path =  "/home/ftam/Downloads/clothing-dataset-small-master/dataset",
data_folders = {'Dress': 'dress', 'Shirt': 'shirt', 'toptee':'toptee'},
n_listings =  300,
prices =  range(5, 120, 5),
unique =  True,
extension =  'jpeg'



def create_listings(request):

    for cate, folder in data_folders.items():
        files = glob(f'{data_path}{os.sep}{data_folders}')
        category = Category.objects.get(name=cate)
        for file in files:
            listing = Listing(title=cate, 
                              price=random.choice(prices),
                              creation_date=datetime.now(),
                              modification_date=datetime.now(),
                              owner=request.user,
                              category=category
                              )
            listing.image = (files, File().read())
    
