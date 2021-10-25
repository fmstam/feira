from django.db import connection
from django.http import response
from django.test import TestCase
from django.test.client import Client
from rest_framework import status



from fair.models import ActivityLog, Category, DeletedData, Listing
from datetime import date, datetime
from django.contrib.auth.models import Group, User

from fair.auth import AuthTools

from faker import Faker



# Create your tests here.

### shortcuts
def create_user(username=Faker().user_name(), 
                email=Faker().ascii_safe_email(), 
                password=Faker().password()):
    
    user = User.objects.create(username=username, 
                                email=email)
    user.set_password(password)
    user.save()

    return user
                
def create_listing(user, title='test listing'):
    return Listing.objects.create( title=title,
                                   creation_date=datetime.now(),
                                   category=Category.objects.last(),
                                   modification_date=datetime.now(),
                                   price=20,
                                   owner=user
                                )
    



### Tests

## Delete and Restore functionalities
class DeleteRestoreListing(TestCase):

    def setUp(self):
        self.user = create_user(username='test user', email='test@localhost', password='12345')
        self.listing = create_listing(title='new listing', user=self.user)
    
    def test_delete_restore(self):
        
        # make sure we have a listing
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(DeletedData.objects.count(), 0)

        # delete it
        id = self.listing.id
        self.listing.delete()
        
        # check it is deleted
        self.assertEqual(Listing.objects.count(), 0)
        self.assertEqual(DeletedData.objects.count(), 1)

        # restore it
        DeletedData.restore_deleted(instance_id=id)

        # make sure we have the listing back
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(DeletedData.objects.count(), 0)
  
## encryption test

class CipherTestCase(TestCase):

    def test_logs_are_encrypted(self):
        """
        Make sure the log activities are encrypted and can be decrypted for revision.
        To that end, we can make an activity, like creating a listing and then,
        check if the activity is recorded and is encrypted.
        """

        self.assertEqual(ActivityLog.objects.count(), 0)
        # make an activity
        user = create_user()
        listing = create_listing(user=user)
        # make sure it is recorded
        self.assertEqual(ActivityLog.objects.count(), 1)

        # let us look at the table entry via a cursor
        action = ActivityLog.objects.last().action
        with connection.cursor() as db_cursor:
            db_cursor.execute(' SELECT action from fair_activitylog')
            encrypted = db_cursor.fetchone()[0]
            print(encrypted)
            self.assertNotEqual(encrypted, action)





## Permission tests
class ListingPerObjectPermissionTestCase(TestCase):

    def setUp(self):
        
        self.auth_user =  create_user(username='auth_user', 
                                     email='auth_user@localhost',
                                     password='12345')

        self.forb_user = create_user(username='forb_user', 
                                     email='forb_user@localhost',
                                     password='12345')



        self.listing = create_listing(title='new listing', user=self.auth_user)


        # initialize permissions
        AuthTools.initialize(sender=None)
                                        


    def test_change_listing(self):
        """
        Test if an ordinary user that owns the listing can modify it while 
        other ordinary users can not.
        """   

        self.assertTrue(
            self.auth_user.has_perm(AuthTools.CHANGE_LISTING, self.listing)
        )

        self.assertFalse(
            self.forb_user.has_perm(AuthTools.CHANGE_LISTING, self.listing)
        )

        # check url authorization
        url =  f'/fair/listings/{self.listing.id}/edit'
        
        # authorized user
        login = self.client.login(username='auth_user', password='12345')
        self.assertTrue(login)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK 
        )

        # forbidden user
        login = self.client.login(username='forb_user', password='12345')
        self.assertTrue(login)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN 
        )

    def test_group_change_listing_permissions(self):

        ## can manager group change ANY listing?
        managers = Group.objects.get(name=AuthTools.MANAGER)
        self.assertTrue(AuthTools.group_has_permission(managers,
                                                       AuthTools.CHANGE_LISTING,
                                                       self.listing))

        ## will an unauthorized user has a group permission if the user joins an authorized group?
        # add the user to the manager group
        self.forb_user.groups.add(managers)
        self.assertTrue(AuthTools.user_has_group_permission(self.forb_user,
                                                            AuthTools.CHANGE_LISTING,
                                                            self.listing))
        # will the user loose the permission when removed from the group
        self.forb_user.groups.remove(managers)
        self.assertFalse(AuthTools.user_has_group_permission(self.forb_user,
                                                            AuthTools.CHANGE_LISTING,
                                                            self.listing))







        
