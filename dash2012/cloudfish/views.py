from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    if request.user.is_authenticated():
        return render(request, 'index_loggedin.html', {'greetings':'Hi!'})
    return render(request, 'index.html')


@login_required
def account(request):
    return render(request, 'account.html', {'active_account': 'active'})

@login_required
def servers(request):
    return render(request, 'servers.html', {'active_servers': 'active'})

def register(request):
    if request.POST:
        #name = request.POST['name']
        username = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['password']
        email = request.POST['email']
        new_user = User.objects.create_user(username, email, password)
        new_user.save()

        user = authenticate(username=username, password=password)
        login(request, user)
    return render(request, 'register.html')