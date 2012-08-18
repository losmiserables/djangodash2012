from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):

    user = User()
    dt_created = models.DateTimeField(auto_now_add=True)
    first_login = models.BooleanField(default=True)