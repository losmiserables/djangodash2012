from django.shortcuts import render


def auth(r):
    return render(r, 'auth.html')

def register(r):
    return render(r, 'index.html')