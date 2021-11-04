"""
    Contains the machine learning classes to handel classification, recommendation, and predictions
"""
# typical imports
import itertools
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from tqdm import tqdm

# sklearn and numpy
from sklearn import metrics
import numpy as np

# torch and image loader
from PIL import Image
from torchvision import transforms, models

# django
from .models import Listing, Similarity
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.db.models import Q


# celery 
from feira.celery import app
import celery
from celery.result import AsyncResult
from celery.states import state, PENDING, SUCCESS, STARTED

class TaskResult():

    def __init__(self,
                task_id,
                task_state='UNKNOWN',
                current_results=None):
        self.task_id = task_id
        self.task_state = task_state
        self.current_results = current_results
    
    @classmethod    
    def collect(cls, results_collector, **kwargs):
        """
            A class method to collect celery tasks' results
            :param: results_collector
        """
        
        if 'task_id' in kwargs.keys():
            task_id = kwargs['task_id']
            response_data = results_collector(task_id)
            task_state = response_data.state
            current_results = response_data.info

            # if not finished yet
            if response_data['state'] != state(SUCCESS):
                # pending or started   
                if (response_data['state'] == state(PENDING)) or (response_data['state'] == state(STARTED)):
                    current_results = None

        snapshot = cls(task_id=task_id,
                      task_state=state,
                      current_results=current_results)
        
        

        

class SimilarityScorer():
    """
    Calculate the similarities between listings and store the similarity scores in a table.
    NOTE: This class requires a two-factor auth which will be added int he next sprint.
    """
    def __init__(self,
                metric=metrics.pairwise.cosine_similarity,
               
                image_input_size=224, # typical input shape for most nets
                feature_extractor=None, # any pytorch nn.module 
                preprocessor=None):

        self.metric = metric
        self.feature_extractor = feature_extractor

        if not self.feature_extractor:
            # efficientnet https://ai.googleblog.com/2019/05/efficientnet-improving-accuracy-and.html
            # B5 acheives quite good with a smaller number of weights compared to others
            # net = models.efficientnet_b5(pretrained=True) 
            
            # OR resnet, which works fine too
            self.net = models.resnet50(pretrained=True) 
            self.net.eval()
            self.return_nodes = {"fc": "fc"} # last layer

        self.feature_extractor =  models.feature_extraction.create_feature_extractor(self.net, 
                                                                                     return_nodes=self.return_nodes)
        
        if not preprocessor:
            self.preprocessor = transforms.Compose([
            transforms.Resize(256), # scale it 
            transforms.CenterCrop(image_input_size), # get the center at the required input shape
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])
        else:
            self.preprocessor = preprocessor

    

    # def add_all_similarities(self, request, calculate=False):
    #     """
    #     Calculate the similarities between all listings and store the scores in the similarly table (see models.py).
    #     It will replace the existing scores in the similarity table.

    #     This way, we do not need to re-calc the features each time the user views a listing.
    #     A simple django query will return the related listings for the current item.
    #     :param: calculate is True the features will be calculated, otherwise the will be loaded from pre-calculated from .npy files in media
    #     """

    #     # An efficient way would be to return a list of id and image tuples,
    #     # and create mini-batches to extract features and calculate scores.
    #     # However, for a large dataset this would require a larage memory.
    #     # A memory friendly, yet a bit slower, is to iterate and calculate
    #     # the similarity between each two listings.
    #     # The similarity matrix/table is symmetric therefore we need to calculate
    #     # it for lower (or upper) traingel of the matrix

    #     # calculate ?
    #     if calculate:
    #         to_features = self.calc_listing_features
    #     else: # otherwise load pre-calculated
    #         to_features = self.load_listing_features

    #     # clear the similarity table
    #     Similarity.objects.all().delete()
        
    #     # order them by pk
    #     listings = Listing.objects.order_by('pk') 

    #     # this loop runs for sum(n-1), where n is the number of listings in the database
    #     for listing_1, listing_2 in tqdm(itertools.combinations(listings, 2)): # unrepeated combinations
    #         # get score
    #         score = self.get_score(to_features(listing_1),
    #                                to_features(listing_1))
    #         # store it
    #         Similarity(score=score, 
    #                   listing_1=listing_1,
    #                   listing_2=listing_2).save()
           
    #     return HttpResponseRedirect(reverse('home'))

    # def update_all_similarities(self, request, calculate=False):
        
    #     """
    #     The same as add_all_similarities but calculate scores of newly added listings and add them to the 
    #     Similarity table.
    #     """

    #     # calculate ?
    #     if calculate:
    #         to_features = self.calc_listing_features
    #     else: # otherwise load pre-calculated
    #         to_features = self.load_listing_features
            
    #     new_listings = Listing.objects.filter(Q(related_listing_1=None) & Q(related_listing_2=None))
    #     exist_listings = Listing.objects.exclude(Q(related_listing_1=None) & Q(related_listing_2=None))
        
    #     # new vs existing
    #     for listing_1 in new_listings:
    #         for listing_2 in tqdm(exist_listings):
    #             # get score
    #             score = self.get_score(to_features(listing_1),
    #                                    to_features(listing_1))
    #             # store it
    #             Similarity(score=score, 
    #                     listing_1=listing_1,
    #                     listing_2=listing_2).save()

    #     # new vs new
    #     for listing_1, listing_2 in tqdm(itertools.combinations(new_listings, 2)): # unrepeated combinations
    #         # get score
    #         score = self.get_score(to_features(listing_1),
    #                                    to_features(listing_1))
    #         # store it
    #         Similarity(score=score, 
    #                   listing_1=listing_1,
    #                   listing_2=listing_2).save()

    #     return HttpResponseRedirect(reverse('home'))

    def calc_listing_features(self, listing, images_path) :
        # read the image
        input_image = Image.open(f'{images_path}{listing.image}')

        # transform the image to fit the model
        input_tensor = self.preprocessor(input_image) 
        input_batch = input_tensor.unsqueeze(0) # add a mini-batch dim. The model expects (batch, channels, width, height)
        
        return  self.feature_extractor(input_batch)['fc'].detach().numpy()



    def get_score (self, listing_1_features, listing_2_features):
        return self.metric(listing_1_features, listing_2_features)


    

    # def load_listing_features(self, listing):
    #     """
    #     Load similarities from npys folder in the media folder 
    #     """
    #     npy_file = f'{self.images_path}{self.npys_name}{os.sep}{listing.id}.npy'
    #     with open(npy_file, 'r') as file:
    #         listing_features = np.load(file)

    #     return listing_features

        
import time 

@app.task(bind=True, ignore_result=False)
# def ml_calc_features(self):
#     i = 0
#     total = 100
#     time.sleep(20)
#     self.update_state(
#                     state='CALC_FEATURES_PROGRESS',
#                     meta={
#                         'current': i,
#                         'total': total,
#                     })
#     i + 1

def ml_calc_features(self):

    """
        Calculate and store features for all images.
    """
    images_path=settings.MEDIA_ROOT
    npys_name='npys' # to store features numpy files 
    replace=False
    scorer = SimilarityScorer()
    # new listings only
    query_set = []
    new_listings = Listing.objects.filter(Q(related_listing_1=None) & Q(related_listing_2=None))
    if new_listings:
        query_set.extend(new_listings.all())
    
    if replace:
        exist_listings = Listing.objects.exclude(Q(related_listing_1=None) & Q(related_listing_2=None))
        query_set.extend(exist_listings.all())
    
    step = 1.0 / len(query_set)
    current = 0
    for listing in query_set:
        # get features
        features = scorer.calc_listing_features(listing, images_path)
        # save them into a npy file
        np.save(f'{images_path}{npys_name}{os.sep}{listing.id}.npy', features)
        self.update_state(
                    state='PROGRESS',
                    meta={
                        'current': current
                    })
        current += step
        print(current)
    return True