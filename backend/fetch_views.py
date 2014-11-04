# coding: utf-8
import logging
from datetime import datetime
from datetime import date
from datetime import timedelta

from underscore import _ as us
from django.db.models import Q
from django import forms
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.db import InternalError
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings 
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_render_json import json
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import SignOrder
from backend import models

logger = logging.getLogger(__name__)

class FilterForm(forms.Form):
    start = forms.DateField(label="start", input_formats=["%Y-%m-%d"], 
        required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    stop = forms.DateField(label="stop", input_formats=["%Y-%m-%d"], 
        required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    
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
@active_tab('fetch')
def fetch(request):
    form = FilterForm(request.GET)
    if not form.is_valid():
        logger.warn("reports, form is invalid, " + str(form.errors))

    stop = form.cleaned_data["stop"]
    stopselect = stop + timedelta(days=1)
    start = form.cleaned_data["start"]
    
    signOrders = SignOrder.objects.filter(create_time__gte=start, create_time__lte=stopselect).order_by('-pk')

    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        dishes = dishes.filter(Q(name__contains=request.GET['q']))
        if not dishes.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)

    table = SignOrderTable(signOrders)
    if search :
        table = SignOrderTable(signOrders, empty_text='没有搜索结果')

    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    form = FilterForm({
        'start': datetime.strftime(start, "%Y-%m-%d"),
        'stop': datetime.strftime(stop, "%Y-%m-%d"),
    })
    return render(request, "backend/fetch.html", {
        'table': table,
        'form': form
    })

class SignOrderTable(tables.Table):
    pk = tables.columns.Column(verbose_name='ID')
    orderid = tables.columns.Column(verbose_name='代取订单号', empty_values=(), orderable=False)
    name = tables.columns.Column(verbose_name='姓名', empty_values=(), orderable=False)
    phone = tables.columns.Column(verbose_name='手机号', empty_values=(), orderable=False)
    address = tables.columns.Column(verbose_name='地址', empty_values=(), orderable=False)
    express = tables.columns.Column(verbose_name='快递公司', empty_values=(), orderable=False)
    create_time = tables.columns.DateTimeColumn(verbose_name='提交时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    statusString = tables.columns.Column(verbose_name='状态', empty_values=(), orderable=False)

    class Meta:
        model = SignOrder
        empty_text = u'没有代取订单'
        fields = ("orderid", "name", "phone", "address", "express", "create_time", "statusString")
        exclude = {'pk'}
        attrs = {
            'class': 'table table-bordered table-striped'
        }

