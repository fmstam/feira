"""
    Contains the machine learning classes to handel classification, recommendation, and predictions
"""
# typical imports
import itertools
import os

# sklearn
from sklearn import metrics.pairwise as metrics

# torch stuff
from PIL import Image
from torchvision import transforms, models

# django
from .models import Listing, Similarity
from django.conf import settings



class SimilarityScorer():
    """
    Calculate the similarities between listing and store them in a table.
    """

    def __init__(self,
                metric=metrics.cosine_similarity,
                images_path=settings.MEDIA_ROOT,
                image_input_size=224, # imagenet input shape
                feature_extractor=None,
                preprocessor=None):

        self.metric = metric
        self.images_path = images_path
        self.feature_extractor = feature_extractor

        if not self.feature_extractor:
            # efficientnet https://ai.googleblog.com/2019/05/efficientnet-improving-accuracy-and.html
            # B5 acheives quite good with a smaller number of weights compared to others
            net = models.efficientnet_b5(pretrained=True) 
        self.feature_extractor =  models.feature_extraction.create_feature_extractor(net)
        
        if not preprocessor:
            self.preprocessor = transforms.Compose([
            transforms.Resize(256), # scale it 
            transforms.CenterCrop(image_input_size), # get the center
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])
        else:
            self.preprocessor = preprocessor
        
    def calc_all_similarities(self):
        """
        Calculate the similarities of all listings and store them in the similarly table (see models.py).
        It will replace the existing scores in the similarity table.

        This way, we do not need to re-calc the feature each time the user views a listing
        A simple django query will return the related listings for the current item.
        """

        # An efficient way would be to return a list of id and image 
        # and create feed mini-batches to extract features and calculate score.
        # however, for a large dataset this would require a larage memory
        # A memory friendly, yet a bit slower, is to iterate and calculate
        # the similarity between each two listings
        # the similarity matrix/table is symmetric therefore we need to calculate
        # it for lower (or upper) traingel of the matrix

        
        # order them by pk
        listings = Listing.objects.order_by('pk') 

        for listing_1, listing_2 in itertools.combinations(listings, 2): # unrepeated combinations
            # get score
            score = self.calc_similarities(listing_1, listing_2)
            # store it
            similarity = Similarity(score=score, 
                                    listing_1=listing_1,
                                    listing_2=listing_2)
            similarity.save()






    def calc_similarities(self, listing_1, listing_2 ):
        """ 
        Calculate the similarity between a two listings
        """

        # nested func to calc the features
        def get_features(listing) :
            # read the image
            input_image = Image.open(f'{self.images_path}{os.sep}{listing.image}')

            # transform the image to fit the model
            input_tensor = self.preprocess(input_image) 
            input_batch = input_tensor.unsqueeze(0) # add a mini-batch dim. The model expects (batch, channels, width, height)
            
            return  self.feature_extractor(input_batch)
        
        # get features
        listing_1_features = get_features(listing=listing_1)
        listing_2_features = get_features(listing=listing_2)

        # get similarities
        score = self.metric(listing_1_features, listing_2_features)

        return score






