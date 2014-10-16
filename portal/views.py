from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "portal/index.html")


def login(request):
    return render(request, "portal/login.html")
    

@login_required
def sign(request):
    return render(request, "portal/index.html")


@login_required
def send(request):
    return render(request, "portal/index.html")


@login_required
def store(request):
    return render(request, "portal/index.html")


@login_required
def profile(request):
    return render(request, "portal/index.html")
