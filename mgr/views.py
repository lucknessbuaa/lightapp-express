# coding: utf-8
from django.shortcuts import render
from base.decorators import active_tab


def signOrdersToFetch(request):
    pass


def signOrdersToDelivery(request):
    pass


@active_tab('send_fetch')
def sendOrdersToFetch(request):
    return render(request, "mgr/sendOrdersToFetch.html")


def sendOrdersToDelivery(request):
    pass   