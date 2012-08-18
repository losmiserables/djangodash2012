"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from cloudfish.models import Cloud
from cloudfish import CLOUD_RACKSPACE

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that the auth_data is correctly signed
        """
        cloud = Cloud(type=CLOUD_RACKSPACE)

