from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from auth.models import Account


def index(request):
    if request.user.is_authenticated():
        return render(request, 'index_loggedin.html', {'greetings': 'Hi!'})
    return render(request, 'index.html')


@login_required
def account(request):
    return render(request, 'account.html', {'active_account': 'active'})


@login_required
def servers(request):
    return render(request, 'servers.html', {'active_servers': 'active'})


@csrf_protect
def register(request):
    c = {}
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        email = request.POST['email']
        if Account.objects.filter(email=email):
            c["errors"] = "This email is already in use."
            return render(request, "register.html", c)

        new_user = Account.objects.create_user(username, email, password)
        new_user.save()

        user = authenticate(username=username, password=password)
        login(request, user)

        request.session['passwd'] = password
        return HttpResponseRedirect(reverse("connect-view"))

    return render(request, 'register.html', c)
