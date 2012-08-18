from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('cloudfish.views',
    url(r'^$', 'index', name='index-view'),
    url(r'^account$', 'account', name='myaccount-view'),
    url(r'^servers$', 'servers', name='myservers-view'),
)