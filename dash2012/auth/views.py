from django.shortcuts import render


def login(r):
    return render(r, 'auth.html')

def register(r):
    return render(r, 'index.html')