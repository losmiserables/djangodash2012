from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html', {'greetings':'Hi!'})
    return render(request, 'index.html')


@login_required(login_url='/auth/login')
def account(request):
    return render(request, 'account.html', {'active_account': 'active'})