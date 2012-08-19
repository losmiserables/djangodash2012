"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from auth.models import Account
from cloudfish.models import Cloud
from cloudfish import CLOUD_RACKSPACE
from django.core.signing import BadSignature
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class KeyEncriptiontest(TestCase):
    def test_encode_decode_auth_data(self):
        """
        Tests that the auth_data is correctly signed
        """
        account = Account(username='daltonmatos', password='mypassword')
        cloud = Cloud(type=CLOUD_RACKSPACE, account=account)

        auth_data = {'user': 'username', 'key': 'my_api_key'}

        _data = cloud.add_auth_data(salt='mypassword', **auth_data)
        self.assertEquals(_data, cloud.auth_data)
        self.assertRaises(BadSignature, cloud.decode_auth_data, salt='worng-salt')
        self.assertEquals(auth_data, cloud.decode_auth_data(salt='mypassword'))


class PrepareSessionTest(TestCase):
    def test_put_auth_data_in_session(self):
        user = Account.objects.create_user(username='name@mail.com', password='pass')
        user.save()

        auth_data = {'user': 'awsuser', 'key': 'mykey'}

        aws = Cloud(type="AM", account=user)
        aws.add_auth_data(salt='pass', **auth_data)
        aws.save()

        self.assertEquals(1, len(Cloud.objects.filter(account=user)))
        self.assertEquals(auth_data, Cloud.objects.filter(account=user)[0].decode_auth_data(salt='pass'))

        client = Client()
        client.post("/auth/login", {"username": 'name@mail.com', "password": "pass"})
        self.assertEquals(auth_data, client.session['clouds']['AM'])


class EmailValidationTest(TestCase):
    def test_unique_email(self):
        account = Account(email="my@email.com", password="mypassword")
        account.save()
        client = Client()
        response = client.post("/register", {"email": "my@email.com", "password": "mypassword", "confirm-password": "mypassword"})

        self.assertIn("This email is already in use.", response.content)


class ConnectOnFirstLoginTest(TestCase):
    def test_redirect_to_connect_if_no_clouds_found(self):
        """
        If the user dows not have any connected cloud backend, redirect to the
        connect view
        """
        user = User.objects.create_user(username='newuser', password='pass')
        user.save()

        client = Client()
        response = client.post("/auth/login", {'username': 'newuser', 'password': 'pass'})
        self.assertIn(reverse('connect-view'), response['Location'])


class ConnectAccountTest(TestCase):
    def test_connect_account(self):
        user = Account.objects.create_user(username="newuser", password="pass")
        user.save()

        client = Client()
        client.post("/auth/login", {'username': 'newuser', 'password': 'pass'})
        client.post("/connect", {"aws_key_id": 1, "aws_secret_key": "my_secrete_key"})

        self.assertEqual(1, Cloud.objects.filter(account=user).count())

    def test_test_cloud(self):
        cloud = Cloud(type=CLOUD_RACKSPACE)
        self.assertFalse(cloud.is_valid(cloud_login='abc', cloud_password='passwd'))
