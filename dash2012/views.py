from django.shortcuts import render


def wait(r):
    return render(r, 'index.html')
