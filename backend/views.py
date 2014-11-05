# -*- coding:utf-8 -*-
import logging
from datetime import datetime
from datetime import date
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.views.decorators.csrf import ensure_csrf_cookie
from django_render_json import render_json, json
from django.views.decorators.http import require_GET

from base.utils import RET_CODES

from django_tables2 import RequestConfig
import django_tables2 as tables
from backend.models import SendOrder
from django import forms
from django.contrib.auth.decorators import user_passes_test
from base.decorators import active_tab
from django.http import HttpResponseRedirect


logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def login(request):
    if request.method == 'GET':
        return render(request, "backend/login.html")
    else:
        user = request.POST.get('username', None)
        password = request.POST.get('password', None)
        logger.debug(password)
        user = auth.authenticate(username=user, password=password)

        if not user:
            return render_json({'ret_code': RET_CODES["auth-failure"]})

        auth.login(request, user)
        return render_json({'ret_code': RET_CODES["ok"]})


def logout(request):
    auth.logout(request)
    return redirect('/backend/login')


def index(request):
    if not request.user.is_authenticated():
        return redirect('/backend/login')
    elif not request.user.is_staff:
        return redirect('/backend/login')
    else:
        return redirect('/backend/fetch')


class ContentTable(tables.Table):
    express = tables.columns.Column(verbose_name='快递公司',orderable=False)
    time = tables.columns.DateTimeColumn(verbose_name='上门日期', orderable=False, format='Y-m-d H:i')
    create_time = tables.columns.DateTimeColumn(verbose_name='创建日期', orderable=False, format='Y-m-d H:i')
    period = tables.columns.Column(verbose_name='收件时间', orderable=False)
    note = tables.columns.Column(verbose_name='备注', orderable=False)

    name = tables.columns.Column(verbose_name=(u'姓名'), orderable=False)
    address = tables.columns.Column(verbose_name=(u'宿舍地址'),orderable=False)
    phone = tables.columns.Column(verbose_name=(u'手机号码'),orderable=False)

    class Meta:
        model=SendOrder
        fields = ('express', 'time', 'create_time','period', 'note', 'name', 'address', 'phone')
        empty_text=('没有代寄订单')
        exclude = {'pk'}
        attrs = {
                'class': 'table table-bordered table-striped'
                }


class FilterForm(forms.Form):
    start = forms.DateField(label='start', input_formats=["%Y-%m-%d"],
            required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    stop = forms.DateField(label='stop', input_formats=["%Y-%m-%d"],
            required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    def clean(self):
        data = super(FilterForm, self).clean()
        stop = data.get("stop", None)
        today = date.today()
        if stop is None:
            stop = today
        if stop > today:
            stop = today

        start = data.get("start", None)
        if start is None:
            start = stop - timedelta(days=7)

        if start > stop:
            start = stop

        return {
            "start": start,
            "stop": stop,
        }


@require_GET
@user_passes_test(lambda u:u.is_staff, login_url='/backend/login')
@active_tab('send')
def send_package(request):
    form = FilterForm(request.GET)
    if not form.is_valid():
        logger.warn("reports, form is invalid, " + str(form.errors))

    stop = form.cleaned_data["stop"]
    stopselect = stop + timedelta(days=1)
    start = form.cleaned_data["start"]

    sorder = SendOrder.objects.filter(create_time__gte=start, create_time__lte=stopselect).order_by('-pk')

    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        dishes = dishes.filter(Q(name__contains=request.GET['q']))
        if not dishes.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)

    table = ContentTable(sorder)
    if search :
        table = SignOrderTable(signOrders, empty_text='没有搜索结果')

    RequestConfig(request).configure(table)
    form = FilterForm({
        'start': datetime.strftime(start, "%Y-%m-%d"),
        'stop': datetime.strftime(stop, "%Y-%m-%d"),
    })


    return render(request, "backend/send.html", {'table': table, 'form':form})

