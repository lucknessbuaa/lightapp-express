# coding: utf-8
import logging

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
from social_auth.db.django_models import UserSocialAuth
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Account

logger = logging.getLogger(__name__)

@require_GET
@active_tab('user')
@user_passes_test(lambda u:u.is_staff, login_url='/backend/login')
def user(request):
    user = Account.objects.filter(user__is_staff=True)
    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        user = user.filter(Q(name__contains=request.GET['q']))
        if not user.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    form = UserForm()
    table = UserTable(user)
    if search :
        table = UserTable(user, empty_text='没有搜索结果')
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "backend/user.html", {
        "table": table,
        "form": form
    })


class UserTable(tables.Table):
    pk = tables.columns.Column(verbose_name='工号', empty_values=(), orderable=False)
    name = tables.columns.Column(verbose_name='姓名', empty_values=(), orderable=False)
    phone = tables.columns.Column(verbose_name='手机号码', empty_values=(), orderable=False)
    create_time = tables.columns.DateTimeColumn(verbose_name='创建时间', empty_values=(), format='Y-m-d H:i:s', orderable=False)
    ops = tables.columns.TemplateColumn(verbose_name='操作', template_name="backend/user_ops.html", orderable=False)
        
    class Meta:
        model = Account
        empty_text = u'没有员工信息'
        fields = ("pk", "name", "phone", "create_time")
        attrs = {
            'class': 'table table-bordered table-striped'
        }

class UserForm(forms.ModelForm):
    name = forms.ModelChoiceField(label=u'待添加员工', queryset=Account.objects.filter(user__is_staff=False),
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    class Meta:
        model = Account


@user_passes_test(lambda u:u.is_staff, login_url='/backend/login')
@json
def delete_user(request):
    user = Account.objects.get(pk=request.POST["id"]);
    staff = User.objects.get(id=user.user.id)
    staff.is_staff = False
    staff.save()

    return {'ret_code': RET_CODES['ok']}

@user_passes_test(lambda u:u.is_staff, login_url='/backend/login')
@json
def edit_user(request, id):
    user = Account.objects.get(id=request.POST["pk"]);
    staff = User.objects.get(id=user.user.id)
    staff.is_staff = True
    staff.save()

    return {'ret_code': RET_CODES['ok']}

@user_passes_test(lambda u:u.is_staff, login_url='/backend/login')
@json
def requireName(request):
    selectName = Account.objects.filter(user__is_staff=False)

    def mapName(name):
        return {
            'id': name.id,
            'text': name.name
        }

    selectName = map(mapName, selectName)
    return{
        'ret_code': RET_CODES['ok'],
        'selectName': selectName
    }
