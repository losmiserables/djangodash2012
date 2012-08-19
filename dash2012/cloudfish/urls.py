from django.conf.urls import patterns, url

urlpatterns = patterns('cloudfish.views',
    url(r'^$', 'index', name='index-view'),
    url(r'^account$', 'account', name='myaccount-view'),
    url(r'^servers$', 'servers', name='myservers-view'),
    url(r'^register$', 'register', name='register-view'),
    url(r'^connect', 'connect', name='connect-view'),
    url(r'^disconnect', 'disconnect', name='disconnect-view'),
    url(r'^create', 'create', name='create-server'),
    url(r'^stop/(?P<provider>[a-zA-Z0-9_.-]+)/(?P<node_id>[a-zA-Z0-9_.-]+)', 'stop', name='stop-server'),
)
