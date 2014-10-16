import logging
import uuid
import requests

from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django_render_json import render_json

from .models import Account


logger = logging.getLogger(__name__)

def updateAccount(user, params):
    account = Account.objects.get(user=user)

    params['authcode'] = account.openid
    resp = requests.post('http://mcsd.sinaapp.com/profile/save', params=params)
    result = resp.json()
    logger.debug('result: %s', str(result))
    if result['code'] != 200:
        raise Exception('api error')


def registerAccount(user):
    openid = str(uuid.uuid4())

    params = {
        'openid': openid,
        'tpid': 2,
        'schoolid': 1,
        'campusid': 1,
        'source': 'baidu_zhidahao',
        'token': 'jinjidexiaoyuan'
    }
    params['openid'] = openid
    resp = requests.post('http://mcsd.sinaapp.com/api/addUser', params=params)
    result = resp.json()
    logger.debug('registerAccount result: %s', str(result))
    if result['code'] != 200:
        return None

    account = Account(user=user, openid=openid)
    account.save()
    return account


def getProfile(user):
    account = Account.objects.get(user=user)
    resp = requests.get('http://mcsd.sinaapp.com/api/getUserInfo', params={
        'authcode': account.openid
    })
    return resp.json()


def isRegistered(user):
    return Account.objects.filter(user=user).count() > 0


def index(request):
    return render(request, "portal/index.html")


def login(request):
    return render(request, "portal/login.html")


def logout(request):
    auth_logout(request)
    return redirect('/app')


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


@csrf_exempt
@login_required
def profile(request):
    if request.method == 'GET':
        profile = {}
        if isRegistered(request.user):
            profile = getProfile(request.user)
            logger.debug('profile: %s', str(profile))

        return render(request, "portal/profile.html", {
            'profile': profile
        })

    if not isRegistered(request.user):
        account = registerAccount(request.user)
        if not account:
            logger.warn('user is not register!')
            return render_json({'ret_code': 1001})
            
    try:
        params = {}
        params.update(request.POST)
        updateAccount(request.user, params)
        return render_json({'ret_code': 0})
    except:
        logger.exception('fail to update account')
        return render_json({'ret_code': 1001})

