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
  <br><b> Figure 2 </b>
</p>

## Current apps:
Feira currently supports two main applications:
 - **fair**: a app where the user can list their items for selling. 
 - **accounts**: a typical django app for account management

### Fair:
 Fair is the core fo the marketplace. It is allows the users to post their items and navigate other users'. 
 
 In the current version, no actual buying functionalities are added but they are in the backlog and will be added in the in the next sprints. The focus was on establishing some different functionalities like ML support, encryption, security. More features and analysis will be added like throttling a flood of request, advanced encryptions, optimization, and more tests especially in the frontend.

 Looking at the current system, we can see the recommendation backend is actually working nice. Here are some examples:

   >> Note: more apps will be added to the project with more machine learning support.