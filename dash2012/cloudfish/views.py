from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def account(request):
    return render(request, 'account.html')