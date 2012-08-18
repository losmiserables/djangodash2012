from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'', include('cloudfish.urls')),

    # Account App
    url(r'^auth/', include('auth.urls')),


)