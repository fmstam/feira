# Feira

A Marketplace powered by machine learning backend services.

Main requirements:
- Python 
- Pytorch
- Django
- SQlite
- Javascript
- HTML 5
- Bootstrap 5

See requirements for a full **conda** environnement setup.


<p align="center">
  <img src="images/main.png">
  <br><b> Marketplace </b>
</p>

## Current apps:
Feira currently supports two main applications:
 - **Fair**: where users can list their items and view other's. 
 - **Accounts**: a typical django app for account management

> Note: more apps will be added to the project with more machine learning support in the next few sprints.

### Fair:
 Currently, Fair is the core of the marketplace. It allows users to post their listings. In the current version, no actual buying functionalities are added but they are in the backlog and will be added in the in the next sprints. The of focus of the last sprint was establishing various functionalities like ML support, encryption, security, and auditing. More features and analysis will be added like throttling a flood of requests, advanced encryptions, optimization, more complex ML support, and more tests especially in the frontend.

 The summary of the some features in the next few sprints include:
 - adding actual buying functionalities
 - performance analysis and traffic optimization
 - customer segmentation and advanced ML services
 - adding more security and permission features
 - more lightweight features, like sharing, rating, ...
 - More API services will be added to support field updating and simple queries.
 - Improving the GUI and add more panels
  

 Looking at the current system, we can easily see the recommendation backend is working quite nice. Here are some examples:

> Note: Many items are generated automatically to populate the system. Therefore, some prices are not realistic. But the actually system is working fine.


> Note: The current recommendation system uses the images only. A hybrid architecture will be developed to include both image, text, and other data types for a more accurate recommendations.

<p align="center">
  <img src="images/recommendations_2.png">
</p>

<p align="center">
  <img src="images/recommendations_3.png">
</p>

<p align="center">
  <img src="images/recommendations_4.png">
</p>
   

<p align="center">
  <img src="images/recommendations_5.png">
</p>


<p align="center">
  <img src="images/recommendations_7.png">
</p>

<p align="center">
  <img src="images/recommendations_8.png">
</p>

<p align="center">
  <img src="images/recommendations_10.png">
</p>

<p align="center">
  <img src="images/recommendations_11.png">
</p>


<p align="center">
  <img src="images/recommendations_ts.png">
</p>

### ML:
The ML backend is quite simple and fast. It uses a pre-trained ***resnet50*** network to extract features and compare them using a similarity metric.

To avoid running the ML every time the user navigates an item. We can run the ML on all items only once. The similarity matrix between all items is calculated only once and whenever the user chooses an item, the system uses a traditional django ORM lookup to show recommendations as shown in the next 
```

          if single: # when viewing a single listing
            listing = get_object_or_404(Listing, **filter) # get the listing
            # and get the recommendations
            # since the table sparse, we compare both fks
            ids = Similarity.objects.filter(Q(listing_1 = listing) | Q(listing_2 = listing)).values_list('listing_1', 'listing_2').order_by('-score')[:5]
            # combine them,
            pks = set([id[0] for id in ids] + [id[1] for id in ids])
            if len(pks) > 0 :
                pks.remove(listing.id)# do not recommend the same listing
            recommendations = Listing.objects.filter(pk__in=pks).all()

            # prepare them for the template 
            listing_dict = {'listing': listing, 
                            'recommendations': recommendations
                            }
```
### Tests:
The current system has some essential features. These include:
- **Security**: auditing, encrypted fields, CSRF tokenization, delete-restore, model and object level permissions. More features like two-factors authentication will be added to some apps.

- **Tests**: some essentials tests were conducted to ensure the system is working fine. These include backend tests like permission tests, CSRF tests, ....


**Summary**: 

The current version is quite simple but is working fine with all tests passed. There are more to be added and explored, especially adding more API-support to the views and focusing more on the front-end.