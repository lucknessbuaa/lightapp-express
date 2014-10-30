# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='\u5bbf\u820d\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='create_time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 30), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.IntegerField(default=0, verbose_name='\u6027\u522b', choices=[(1, '\u7537'), (0, '\u5973')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default=datetime.date(2014, 10, 30), max_length=255, verbose_name='\u59d3\u540d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=255, null=True, verbose_name='\u624b\u673a\u53f7\u7801'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
