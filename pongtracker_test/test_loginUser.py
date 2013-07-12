'''
Created on 2013 7 11

@author: Student
'''
import unittest
from mock import MagicMock
from django.contrib.auth.models import User
from User.views import * 
from django.test.client import RequestFactory



class UserViewTests(unittest.TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(first_name='jacob', email='jacob@…', password='top_secret')
        
        pass


    def tearDown(self):
        self.user.delete()
        pass


    def loginUser_validUser(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')

        # Recall that middleware are not suported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = my_view(request)
        self.assertEqual(response.status_code, 200)
          
              
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()