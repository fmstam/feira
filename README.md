# Feira

A Marketplace powered by machine learning backend services.

Main requirements:
- Python 
- Pytorch
- Django
- SQLite
- Javascript
- HTML 5
- Bootstrap 5

**To run:** you can use the Dockerfile


<p align="center">
  <img src="images/main.png">
  <br><b> Marketplace </b>
</p>

## Current apps:
Feira currently supports two main applications:
 - **Fair**: where users can list their items for selling. 
 - **Accounts**: a typical app for account management

> Note: more apps will be added to the project with more machine learning support in the next few sprints.

### Fair:
 Currently, Fair is the core of the marketplace. It allows users to post their listings. In the current version, no actual buying functionalities are added but they are in the backlog and will be added in the in the next sprints. The focus of the last sprint (two weeks) was establishing various functionalities like ML support, encryption, security, and auditing. More features and traffic analysis will be added like throttling a flood of requests, advanced encryptions, optimization, advanced ML support, and more tests especially in the frontend.

 The summary of some features that will be added in the next few sprints include:
 - adding actual buying functionalities
 - performance analysis and traffic optimization
 - customer segmentation and advanced ML services
 - adding more security and permission features
 - more lightweight features, like sharing, rating, ...
 - More API services will be added to support field updating and simple queries.
 - Improving the frontend and add more panels
  

 Looking at the current version, we can easily see the recommendation backend is working quite nice. Here are some examples:

```
  
  celery -A feira worker -l INFO

```
> Note: Many items are generated automatically to populate the system. Therefore, some prices are not realistic :)


> Note: The current recommendation system uses the images only. A hybrid architecture will be developed to include both image, text, and other data types for a better accurate predictions.

<p align="center">
  <img src="images/recommendations_1.png">
</p>

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
  <img src="images/recommendations_6.png">
</p>

<p align="center">
  <img src="images/recommendations_7.png">
</p>


### You may also like:
In order to populate the system with data, the fashion dataset: https://github.com/XiaoxiaoGuo/fashion-iq was used to create dummy listings. This will make it reasonable to check how the system will look like in production. You can try your own settings by changing the *configurations.json* file in the *fair* app.

The ML backend is quite simple and fast. It uses a pre-trained ***resnet50*** network to extract features and compare them using a similarity metric.

To avoid running the ML service every time the user navigates an item, which is not practical nor necessary, we can run the ML on all items only once. The similarity matrix between all items is calculated and whenever the user chooses an item, the system uses a simple and clean django ORM lookup to show recommendations. This separation reduces dependencies between django and ML libs and make future extensions (e.g. a more robust recommendation ML) easy to add. However, for some other ML services this is not possible and API-based interaction will be used (e.g., using FastAPI)

The similarity matrix, will be updated once new items are posted on the systems. One way to do it would be to run a background service after the post-saving signal. However, that might lead to a racing-condition between ML and db engines and would require proper synchronization and locking. Another efficient and simple approach is to update them using an explicit command that takes care of the system existing state and ensure data integrity pre-during- and-post update.

### Security:
The current system has some essential features like auditing, encrypted fields, CSRF tokenization, delete-restore, model and object level permissions. More features like two-factors authentication will be added to some apps.


### Tests:
Some essentials tests were conducted to ensure the system is working fine. These include backend tests like permission tests, CSRF tests, ....


### Summary:
The current version is quite simple but is working fine with all tests went OK. There are more to be added and explored, especially adding more API-support to the views and focusing more on the front-end. 