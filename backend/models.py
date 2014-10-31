# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    (1, u'男'),
    (0, u'女')
)

class Account(models.Model):
    user = models.ForeignKey(User)
    points = models.IntegerField(default=0)
    gender = models.IntegerField(verbose_name=u'性别', choices=GENDER_CHOICES, default=0)
    name = models.CharField(verbose_name=u'姓名', max_length=255)
    address = models.CharField(verbose_name=u'宿舍地址', null=True, max_length=255)
    phone = models.CharField(verbose_name=u'手机号码', null=True, max_length=255)

    create_time = models.DateTimeField(auto_now_add=True)


EXPRESS_CHOICES = (
    (6, u'百世汇通'),
    (5, u'顺丰'),
)

class SendOrder(models.Model):
    account = models.ForeignKey(Account)
    express = models.IntegerField(verbose_name=u'快递公司', choices=EXPRESS_CHOICES)
    time = models.DateTimeField(verbose_name=u'上门日期')
    period = models.CharField(verbose_name=u'收件时间', max_length=255)
    note = models.CharField(verbose_name=u'备注', max_length=255, null=True)

    name = models.CharField(verbose_name=u'姓名', max_length=255)
    address = models.CharField(verbose_name=u'宿舍地址', null=True, max_length=255)
    phone = models.CharField(verbose_name=u'手机号码', null=True, max_length=255)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def status(self):
        return 0

    def statusString(self):
        return u'处理中'

    def orderid(self):
        return 'SD#%d' % (2000 + self.pk)


SIGN_EXPRESS_CHOICES = (
    (1, u'圆通'),
    (2, u'中通'),
    (3, u'申通'),
    (4, u'韵达'),
    (5, u'顺丰'),
    (6, u'百世汇通'),
    (7, u'EMS'),
    (8, u'天天'),
    (9, u'晟邦'),
    (10, u'亚马逊'),
    (12, u'唯品会'),
    (13, u'中国邮政'),
    (16, u'京东'),
    (100, u'其它公司')
)

class SignOrder(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(verbose_name=u'姓名', max_length=255)
    address = models.CharField(verbose_name=u'宿舍地址', null=True, max_length=255)
    phone = models.CharField(verbose_name=u'手机号码', null=True, max_length=255)
    express = models.IntegerField(verbose_name=u'快递公司', choices=SIGN_EXPRESS_CHOICES)
    note = models.CharField(verbose_name=u'备注', max_length=255, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def status(self):
        return 0

    def statusString(self):
        return u'处理中'


    def orderid(self):
        return 'SN#%d' % (2000 + self.pk)


class StoreItem(models.Model):
    points = models.IntegerField()


class StormItemOrder(models.Model):
    points = models.IntegerField()
    account = models.ForeignKey(Account)

