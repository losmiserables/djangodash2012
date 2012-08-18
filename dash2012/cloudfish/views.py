from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
        pass
    return render(request, 'register.html')