# -*- coding: utf-8 -*-  
import logging
import json
import datetime
import uuid
import requests

from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django_render_json import render_json
import django_auth_json

from backend.models import Account, SendOrder, SignOrder

logger = logging.getLogger(__name__)
API_TOKEN = 'jinjidexiaoyuan'


def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def addPoints(account):
    account.points = accout.points + 200
    account.save()


def updateAccount(user, params):
    account = Account.objects.get(user=user)
    account.name = params.get('name')
    account.phone = params.get('phone')
    account.address = params.get('address')
    account.gender = params.get('gender')
    account.save()

def registerAccount(user):
    account = Account(user=user)
    account.save()
    return account


def getProfile(user):
    return forms.model_to_dict(Account.objects.get(user=user))


def isRegistered(user):
    return Account.objects.filter(user=user).count() > 0


def index(request):
    logger.debug('welcome to nankuaidi')
    return render(request, "portal/index.html")


def login(request):
    return render(request, "portal/login.html")


def logout(request):
    auth_logout(request)
    return redirect('/app')


@login_required
def sign(request):
    try:
        profile = getProfile(request.user)
    except:
        profile = {}

    return render(request, "portal/sign.html", {
        'profile': profile
    })


@login_required
def send(request):
    days = []
    now = datetime.datetime.now()
    for i in range(0, 5):
        days.append(now + datetime.timedelta(days=i))
    return render(request, "portal/send.html", {
        'days': days
    })


@csrf_exempt
def addSendOrder(request):
    if not isRegistered(request.user):
        return render_json({
            'ret_code': 1002,
            'msg': 'error!'
        })

    account = Account.objects.get(user=request.user)

    params = request.POST
    time = datetime.datetime.today() + datetime.timedelta(days=int(params.get('fetchdate')))
    SendOrder(account=account, time=time, period=params.get('fetchperiod'),
            note=params.get('notes'), express=params.get('company')).save()
    return render_json({'ret_code': 0})


class SignOrderForm(forms.ModelForm):
    class Meta:
        model = SignOrder


@csrf_exempt
def addSignOrder(request):
    if not isRegistered(request.user):
        return render_json({
            'ret_code': 1002,
            'msg': 'error!'
        })

    account = Account.objects.get(user=request.user)

    params = {}
    params.update(request.POST)
    params['account'] = account.pk
    params['express'] = int(params['express'][0])
    logger.debug('params: %s', params)

    form = SignOrderForm(params)
    if not form.is_valid():
        logger.warn("form is invalid: %s", form.errors)
        return render_json({'ret_code': 1001, 'msg': '参数不正确'})

    form.save()
    return render_json({'ret_code': 0})


def store(request):

    params = {'limit':30}
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoods', params=params)
    goods = resp.json()
    goods = filter(lambda good: good['goodsid'] != 2, goods)

    return render(request, "portal/store.html", {'goods':goods})


def storeItem(request):
    goodsid = int(request.GET.get('goodsid'))
    params = {'goodsid':goodsid}
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoodsById', params=params)
    good = resp.json()
    good['remain'] = good['num'] - good['consumption']
    good['ratingRange'] = range(good['rating'])

    return render(request, "portal/item.html", {'good':good})


@csrf_exempt
@django_auth_json.login_required({'code': 12580})
def doOrder(request):
    if not isRegistered(request.user):
        return render_json({'code':302, 'msg':'请先完善个人信息'})

    account = Account.objects.get(user=request.user)
    params = {}
    params.update(request.POST)
    params.update({
        'authcode': account.openid
    })
    resp = requests.post('http://mcsd.sinaapp.com/tmall/doOrder', params = params)
    result = resp.json()
    return render_json(result)


@login_required
def getOrder(request):
    if not isRegistered(request.user):
        return render(request, "portal/myOrder.html", {'orders':[]})
    
    account = Account.objects.get(user=request.user)
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoodsOrder', params={
        'authcode': account.openid
    })
    result = resp.json()
    
    for item in result:
        item['time'] = datetime.datetime.strptime(item['createtime'],'%b %d, %Y %I:%M:%S %p')
    return render(request, "portal/myOrder.html", {'orders':result})


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

    pointsGot = False
    if not isRegistered(request.user):
        account = registerAccount(request.user)
        if not account:
            logger.warn('user is not register!')
            return render_json({'ret_code': 1001})
            
        addPoints(account)
        pointsGot = True

    try:
        updateAccount(request.user, request.POST)
        return render_json({
            'ret_code': 0,
            'points_got': pointsGot
        })
    except:
        logger.exception('fail to update account')
        return render_json({'ret_code': 1001})


def rule(request):
    return render(request, 'portal/rule.html')



def getRecentSendOrders(user):
    try:
        return requests.get('http://mcsd.sinaapp.com/api/getOrder', params={
            'type': 1,
            'authcode': Account.objects.get(user=user).openid
        }).json()
    except:
        return []


def getRecentSignOrders(user):
    try:
        return requests.get('http://mcsd.sinaapp.com/api/getOrder', params={
            'type': 0,
            'authcode': Account.objects.get(user=user).openid
        }).json()
    except:
        return []


@login_required
def recent(request):
    signOrders = getRecentSignOrders(request.user)
    sendOrders = getRecentSendOrders(request.user)
    logger.debug(signOrders)
    logger.debug(sendOrders)
    for item in signOrders:
        item['createtime'] = datetime.datetime.strptime(item['createtime'], '%b %d, %Y %H:%M:%S %p')
    for item in sendOrders:
        item['createtime'] = datetime.datetime.strptime(item['createtime'], '%b %d, %Y %H:%M:%S %p')
    
    return render(request, 'portal/recent.html', {
        'signOrders': signOrders,
        'sendOrders': sendOrders
    })


def deleteRecentPackage(user, id):
    try:
        return requests.post('http://mcsd.sinaapp.com/order/cancel', params={
            'authcode': user,
            'orderid': id
        }).json()
    except:
        return []


@csrf_exempt
@login_required
def deleteRecent(request):
    account = Account.objects.get(user=request.user)
    authcode = account.openid

    return render_json({'retValue': deleteRecentPackage(authcode, request.POST['orderid'])})


def points(request):
    return render(request, 'portal/points.html')


def error500(request):
    return render(request, 'portal/error.html', status=500)


def error(request):
    raise


def price(request):
    return render(request, 'portal/price.html')

