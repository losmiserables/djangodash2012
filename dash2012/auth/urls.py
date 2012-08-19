from django.conf.urls import patterns, url

urlpatterns = patterns('auth.views',
    url(r'^login$', 'login', name='login-view'),
    url(r'^logout$', 'logout', name='logout-view'),
)