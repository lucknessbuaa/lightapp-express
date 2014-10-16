from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Account


def isRegistered(user):
    return Account.objects.filter(user=user).count() > 0


def index(request):
    return render(request, "portal/index.html")


def login(request):
    return render(request, "portal/login.html")
    

@login_required
def sign(request):
    if not isRegistered(request.user):
        return redirect('/app/profile')

    return render(request, "portal/sign.html")


@login_required
def send(request):
    if not isRegistered(request.user):
        return redirect('/app/profile')

    return render(request, "portal/send.html")


@login_required
def store(request):
    if not isRegistered(request.user):
        return redirect('/app/profile')

    return render(request, "portal/store.html")


@login_required
def profile(request):
    return render(request, "portal/profile.html")

