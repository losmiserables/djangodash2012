from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from cloudfish.models import Cloud


def login(r):
    if r.POST:
        username = r.POST['username']
        password = r.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(r, user)
            if not Cloud.objects.filter(account=user).exists():
                return HttpResponseRedirect(reverse('connect-view'))

            return HttpResponseRedirect(reverse('myservers-view'))

    return render(r, 'auth.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index-view'))


@login_required
def connect(request):
    return render(request, 'connect.html')
