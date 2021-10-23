from django.http import response
from django.test import TestCase
from django.test.client import Client
from rest_framework import status



from fair.models import Category, Listing
from datetime import date, datetime
from django.contrib.auth.models import User


# Create your tests here.


# permission tests
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

                                        


    def test_update_listing(self):
        from fair.auth import AuthenticationManager
        listing = Listing.objects.create(
            title='test_listing',
            creation_date=datetime.now(),
            category=Category.objects.last(),
            modification_date=datetime.now(),
            price=20,
            owner=self.auth_user
        )

        AuthenticationManager.initialize(sender=self)

        self.assertTrue(
            self.auth_user.has_perm(AuthenticationManager.CHANGE_LISTING, listing)
        )

        self.assertFalse(
            self.forb_user.has_perm(AuthenticationManager.CHANGE_LISTING, listing)
        )

        # check url authorization
        url =  f'/fair/listings/{listing.id}/edit'
        data = {'title': 'new listing updated'}

        
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
        