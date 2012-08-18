from django.db import models
from cloudfish import SUPPORTED_CLOUDS
from auth.models import Account

class Cloud(models.Model):

    type = models.CharField(max_length=32, choices=SUPPORTED_CLOUDS)

    # This is a JSON content, encrypted using the users password.
    # Must be re-generated every time the user changes its password.
    auth_data = models.CharField(max_length=1024)

    account = models.ForeignKey(Account, related_name='clouds')

