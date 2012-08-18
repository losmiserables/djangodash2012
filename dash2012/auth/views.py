from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login(r):
    if r.POST:
        username = r.POST['username']
        password = r.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(r, user)
            return HttpResponseRedirect(reverse('myservers-view'))

    return render(r, 'auth.html')

def register(r):
    if r.POST:

        pass
    return render(r, 'register.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index-view'))