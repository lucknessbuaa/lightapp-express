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

from backend.models import Account, SendOrder, SignOrder, Goods, GoodOrder

logger = logging.getLogger(__name__)
API_TOKEN = 'jinjidexiaoyuan'


def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def addPoints(account):
    account.points = account.points + 200
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
    if request.user.is_staff:
        return redirect("/mgr/sign/fetch")
    else:
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
    SendOrder(account=account, time=time, 
            name=account.name, address=account.address, phone=account.phone,
            period=params.get('fetchperiod'),
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

    request.POST = request.POST.copy()
    request.POST['account'] = account.pk
    request.POST['express'] = int(request.POST['express'][0])
    request.POST['status'] = 0
    form = SignOrderForm(request.POST)
    if not form.is_valid():
        logger.warn("form is invalid: %s", form.errors)
        return render_json({'ret_code': 1001, 'msg': '参数不正确'})

    form.save()
    return render_json({'ret_code': 0})


def store(request):
    gs =  Goods.objects.all().values()

    return render(request, "portal/store.html", {'goods':gs})


def storeItem(request):
    goodsid = int(request.GET.get('goodsid'))
    params = {'goodsid':goodsid}
    good = Goods.objects.filter(goodsid=goodsid)
    good = good.values()[0]
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
    
    params.update({'account_id':account.id})
    params.update({'status':0})
    
    for k in params:
        if type(params[k]) == type([]):
            params[k] = params[k][0]

    goods = Goods.objects.filter(goodsid=params['goodsid'])
    if len(goods) <= 0:
        return render_json({'code':902,'msg':u'商品不存在'})
    goods = goods[0]
    if goods.num-goods.consumption <= 0:
        return render_json({'code':904, 'msg':u'商品库存不足'})
    points_needed = goods.points*int(params['num'])
    if points_needed > account.points:
        return render_json({'code':820, 'msg':u'用户积分不足'})
    total_price = goods.price*int(params['num'])
    total_points = goods.points* int(params['num'])
    params.pop('goodsid')
    params.update({'goods_id': goods.id})
    params.update({'total_price': total_price})
    params.update({'total_points': total_points})
    gOrder = GoodOrder(**params)
    account.points -= points_needed
    goods.consumption += int(params['num'])
    gOrder.save()
    account.save()
    goods.save()

    return render_json({'code':200})


@login_required
def getOrder(request):
    if not isRegistered(request.user):
        return render(request, "portal/myOrder.html", {'orders':[]})
    
    account = Account.objects.get(user=request.user)
    gOrder = GoodOrder.objects.filter(account_id=account.id).order_by('-pk').values()
    gOrder = list(gOrder)
    '''
    resp = requests.get('http://mcsd.sinaapp.com/api/getGoodsOrder', params={
        'authcode': account.openid
    })
    result = resp.json()
    print result
    
    for item in result:
        item['time'] = datetime.datetime.strptime(item['create_time'],'%b %d, %Y %I:%M:%S %p')
    '''
    result = gOrder
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
    return SendOrder.objects.filter(account__user=user).order_by('-create_time')[:7]


def getRecentSignOrders(user):
    return SignOrder.objects.filter(account__user=user).order_by('-create_time')[:7]


@login_required
def recent(request):
    signOrders = getRecentSignOrders(request.user)
    sendOrders = getRecentSendOrders(request.user)
    
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
    if request.POST.get('type') == 'sign':
        SignOrder.objects.filter(pk=request.POST.get('orderid')).delete()
    else:
        SendOrder.objects.filter(pk=request.POST.get('orderid')).delete()

    return render_json({'retValue': {'code': 200}})


def points(request):
    return render(request, 'portal/points.html')


def error500(request):
    return render(request, 'portal/error.html', status=500)


def error(request):
    raise


def price(request):
    return render(request, 'portal/price.html')

