# -*- coding: utf-8 -*-  
import logging
import datetime
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

    return render(request, "portal/sign.html")


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

    params = {}
    params.update(request.POST)
    params.update({
        'authcode': account.openid
    })
    logger.debug('add send order, params: \n%s', str(params))

    resp = requests.post('http://mcsd.sinaapp.com/order/save', params=params)
    result = resp.json()
    if result['code'] == 200:
        return render_json({'ret_code': 0})
    else:
        return render_json({
            'ret_code': 1001,
            'msg': result['msg']
        })


@login_required
def store(request):

    params = {'limit':30}
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoods', params = params)
    goods = resp.json()

    return render(request, "portal/store.html", {'goods':goods})

@login_required
def storeItem(request):
    if not isRegistered(request.user):
        return redirect('/app/profile')

    goodsid = int(request.GET.get('goodsid'))
    params = {'goodsid':goodsid}
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoodsById', params = params)
    good = resp.json()
    good['remain'] = good['num'] - good['consumption']
    good['ratingRange'] = range(good['rating'])

    return render(request, "portal/item.html", {'good':good})


@csrf_exempt
@login_required
def doOrder(request):
    if not isRegistered(request.user):
        return {'code':302, 'msg':'请先完善个人信息'}

    params = {}
    params.update(request.POST)
    resp = requests.post('http://mcsd.sinaapp.com/tmall/doOrder', params = params)
    result = resp.json()
    return render_json(result)


@login_required
def getOrder(request):
    if not isRegistered(request.user):
        return redirect('/app/profile')
    
    account = Account.objects.get(user=request.user)
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoodsOrder', params={
        'authcode': account.openid
    })
    result = resp.json()
    
    # for item in result:
    #     item['time'] = datetime.datetime.strptime(item['createtime'],'%M %j, %Y')
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
    return render(request, 'portal/recent.html', {
        'signOrders': getRecentSignOrders(request.user),
        'sendOrders': getRecentSendOrders(request.user)
    })

