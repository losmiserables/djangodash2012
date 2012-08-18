from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^$', 'cloudfish.views.index', name='index-view'),
    url(r'^account$', 'cloudfish.views.account', name='myaccount-view'),

    # Account App
    url(r'^auth/', include('auth.urls')),

)