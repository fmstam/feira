from django.http import response
from django.test import TestCase
from django.test.client import Client
from rest_framework import status



from fair.models import Category, Listing
from datetime import date, datetime
from django.contrib.auth.models import Group, User

from fair.auth import AuthTools


# Create your tests here.


## Permission tests
class ListingPerObjectPermissionTestCase(TestCase):
    @classmethod
    def setUp(self):
        
        self.auth_user = User.objects.create(username='auth_user', 
                                            email='auth_user@localhost')
        self.auth_user.set_password('12345')
        self.auth_user.save()

        self.forb_user = User.objects.create(username='forb_user', 
                                            email='forb_user@localhost')
        self.forb_user.set_password('12345')
        self.forb_user.save()


        self.listing = Listing.objects.create(
            title='test_listing',
            creation_date=datetime.now(),
            category=Category.objects.last(),
            modification_date=datetime.now(),
            price=20,
            owner=self.auth_user
            )


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







        
