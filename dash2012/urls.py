from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^$', 'cloudfish.views.index', name='index-view'),

    # Account App
    url(r'^account/', include('account.urls')),

)