# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User)
    points = models.IntegerField()


class SendOrder(models.Model):
    account = models.ForeignKey(Account)


class SignOrder(models.Model):
    account = models.ForeignKey(Account)


class StoreItem(models.Model):
    points = models.IntegerField()


class StormItemOrder(models.Model):
    points = models.IntegerField()
    account = models.ForeignKey(Account)

