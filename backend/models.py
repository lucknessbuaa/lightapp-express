# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    (1, u'男'),
    (0, u'女')
)

class Account(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(verbose_name=u'姓名', max_length=255)
    points = models.IntegerField(default=0)
    gender = models.IntegerField(verbose_name=u'性别', choices=GENDER_CHOICES, default=0)
    address = models.CharField(verbose_name=u'宿舍地址', null=True, max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(verbose_name=u'手机号码', null=True, max_length=255)


class SendOrder(models.Model):
    account = models.ForeignKey(Account)


class SignOrder(models.Model):
    account = models.ForeignKey(Account)


class StoreItem(models.Model):
    points = models.IntegerField()


class StormItemOrder(models.Model):
    points = models.IntegerField()
    account = models.ForeignKey(Account)

