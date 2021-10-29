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




class SimilarityScorer(LoginRequiredMixin):
    """
    Calculate the similarities between listings and store the similarity scores in a table.
    NOTE: This class requires a two-factor auth which will be added int he next sprint.
    """
    def __init__(self,
                metric=metrics.pairwise.cosine_similarity,
                images_path=settings.MEDIA_ROOT,
                npys_name='npys', # to store features numpy files
                image_input_size=224, # typical input shape for most nets
                feature_extractor=None,
                preprocessor=None):

        self.metric = metric
        self.images_path = images_path
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

    def calc_features(self, request, replace=True):
        """
        Calculate and store features for all images.
        """

        new_listings = Listing.objects.filter(Q(related_listing_1=None) & Q(related_listing_2=None))
        query_sets = [new_listings]
        if replace:
            exist_listings = Listing.objects.exclude(Q(related_listing_1=None) & Q(related_listing_2=None))
            query_sets.extend(exist_listings)
        
        for query_set in query_sets:
            for listing in query_set:
                # get features
                features = self.calc_features(listing)
                # save them into a npy file
            np.save(f'{self.images_path}{self.npys_name}{os.sep}{listing.id}.npy',features)


    def add_all_similarities(self, request):
        """
        Calculate the similarities between all listings and store the scores in the similarly table (see models.py).
        It will replace the existing scores in the similarity table.

        This way, we do not need to re-calc the features each time the user views a listing.
        A simple django query will return the related listings for the current item.
        """

        # An efficient way would be to return a list of id and image tuples,
        # and create mini-batches to extract features and calculate scores.
        # However, for a large dataset this would require a larage memory.
        # A memory friendly, yet a bit slower, is to iterate and calculate
        # the similarity between each two listings.
        # The similarity matrix/table is symmetric therefore we need to calculate
        # it for lower (or upper) traingel of the matrix

        # clear the similarity table
        Similarity.objects.all().delete()
        
        # order them by pk
        listings = Listing.objects.order_by('pk') 

        # this loop runs for sum(n-1), where n is the number of listings in the database
        for listing_1, listing_2 in tqdm(itertools.combinations(listings, 2)): # unrepeated combinations
            # get score
            score = self.calc_similarities(listing_1, listing_2)
            # store it
            Similarity(score=score, 
                      listing_1=listing_1,
                      listing_2=listing_2).save()
           
        return HttpResponseRedirect(reverse('home'))

    def update_all_similarities(self, request):
        
        """
        The same as add_all_similarities but calculate scores of newly added listings and add them to the 
        Similarity table.
        """

        new_listings = Listing.objects.filter(Q(related_listing_1=None) & Q(related_listing_2=None))
        exist_listings = Listing.objects.exclude(Q(related_listing_1=None) & Q(related_listing_2=None))
        
        # new vs existing
        for listing_1 in new_listings:
            for listing_2 in tqdm(exist_listings):
                # get score
                score = self.calc_similarities(listing_1, listing_2)
                # store it
                Similarity(score=score, 
                        listing_1=listing_1,
                        listing_2=listing_2).save()

        # new vs new
        for listing_1, listing_2 in tqdm(itertools.combinations(new_listings, 2)): # unrepeated combinations
            # get score
            score = self.calc_similarities(listing_1, listing_2)
            # store it
            Similarity(score=score, 
                      listing_1=listing_1,
                      listing_2=listing_2).save()

        return HttpResponseRedirect(reverse('home'))



    def listing_to_feature(self, listing) :
        # read the image
        input_image = Image.open(f'{self.images_path}{listing.image}')

        # transform the image to fit the model
        input_tensor = self.preprocessor(input_image) 
        input_batch = input_tensor.unsqueeze(0) # add a mini-batch dim. The model expects (batch, channels, width, height)
        
        return  self.feature_extractor(input_batch)


    def calc_similarities(self, listing_1, listing_2 ):
        """ 
        Calculate the similarity between two listings
        """

        # get features
        listing_1_features = self.listing_to_feature(listing=listing_1)['fc'].detach().numpy()
        listing_2_features = self.listing_to_feature(listing=listing_2)['fc'].detach().numpy()

        # get similarities
        score = self.metric(listing_1_features, listing_2_features)

        return score