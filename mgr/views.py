# coding: utf-8
import time
import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
import django.contrib.auth as auth

from django_render_json import render_json
from base.decorators import active_tab
from backend.models import SendOrder, SignOrder


logger = logging.getLogger(__name__)

@user_passes_test(lambda u:u.is_staff, login_url='/app/')
@active_tab('sign_fetch')
def signOrdersToFetch(request):
    orders = SignOrder.objects.filter(status=SignOrder.ORDER_INITIAL)
    logger.debug('sign orders count: %d', orders.count())
    return render(request, 'mgr/signOrdersToFetch.html', {'orders': orders})

@user_passes_test(lambda u:u.is_staff, login_url='/app/')
@active_tab('sign_delivery')
def signOrdersToDelivery(request):
    orders = SignOrder.objects.filter(status=SendOrder.ORDER_RECEIVED)
    logger.debug('sign orders count: %d', orders.count())
    return render(request, 'mgr/signOrdersToSend.html', {'orders': orders})


@user_passes_test(lambda u:u.is_staff, login_url='/app/')
@active_tab('send_fetch')
def sendOrdersToFetch(request):
    orders = SendOrder.objects.filter(status=SendOrder.ORDER_INITIAL)
    logger.debug('orders count: %d', orders.count())
    return render(request, "mgr/sendOrdersToFetch.html", {
        'orders': orders
    })


@user_passes_test(lambda u:u.is_staff, login_url='/app/')
@active_tab('send_send')
def sendOrdersToDelivery(request):
    orders = SendOrder.objects.filter(status=SendOrder.ORDER_RECEIVED)
    logger.debug('orders count: %d', orders.count())
    return render(request, "mgr/sendOrdersToSend.html", {
        'orders': orders
    })

@require_POST
@csrf_exempt
def receiveSignOrder(request):
    id = request.POST.get('id')

    if not id:
        return render_json({
            'ret_code': 1001
        })
    order = SignOrder.objects.filter(status=SignOrder.ORDER_INITIAL, pk=id)
    order.update(status=SendOrder.ORDER_RECEIVED)
    
    return render_json({
        'ret_code': 0
    })

@require_POST
@csrf_exempt
def refuseSignOrder(request):
    id = request.POST.get('id')

    if not id:
        return render_json({'ret_code': 1001})

    order = SignOrder.objects.filter(status=SignOrder.ORDER_INITIAL, pk=id)
    order.update(status=SendOrder.ORDER_CANCELED)

    return render_json({'ret_code': 0})

@require_POST
@csrf_exempt
def receiveSendOrder(request):
    id = request.POST.get('id')

    if not id:
        return render_json({
            'ret_code': 1001
        })

    order = SendOrder.objects.filter(status=SendOrder.ORDER_INITIAL, pk=id)
    order.update(status=SendOrder.ORDER_RECEIVED)

    return render_json({
        'ret_code': 0
    })

@require_POST
@csrf_exempt
def completeSignOrder(request):
    id = request.POST.get('id')
    price = request.POST.get('price')

    if not id or not price:
        return render_json({
            'ret_code': 1001
        })

    try:
        price = float(price)
    except:
        return render_json({
            'ret_code': 1001
        })



    order = SignOrder.objects.filter(status=SendOrder.ORDER_RECEIVED, pk=id)
    order.update(status=SendOrder.ORDER_SENT, price=price)
    

    return render_json({'ret_code': 0 })

@require_POST
@csrf_exempt
def completeSendOrder(request):
    id = request.POST.get('id')
    order_no = request.POST.get('order_no')

    if not id or not order_no:
        return render_json({
            'ret_code': 1001
        })

    order = SendOrder.objects.filter(status=SendOrder.ORDER_RECEIVED, pk=id)
    order.update(status=SendOrder.ORDER_SENT, order_no=order_no)

    return render_json({
        'ret_code': 0
    })


def logout(request):
    auth.logout(request)
    return redirect('/app/')
