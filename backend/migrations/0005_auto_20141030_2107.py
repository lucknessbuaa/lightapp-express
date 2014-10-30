# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20141030_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='signorder',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='\u5bbf\u820d\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='signorder',
            name='create_time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 30), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signorder',
            name='express',
            field=models.IntegerField(default=100, verbose_name='\u5feb\u9012\u516c\u53f8', choices=[(1, '\u5706\u901a'), (2, '\u4e2d\u901a'), (3, '\u7533\u901a'), (4, '\u97f5\u8fbe'), (5, '\u987a\u4e30'), (6, '\u767e\u4e16\u6c47\u901a'), (7, 'EMS'), (8, '\u5929\u5929'), (9, '\u665f\u90a6'), (10, '\u4e9a\u9a6c\u900a'), (12, '\u552f\u54c1\u4f1a'), (13, '\u4e2d\u56fd\u90ae\u653f'), (16, '\u4eac\u4e1c'), (100, '\u5176\u5b83\u516c\u53f8')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signorder',
            name='name',
            field=models.CharField(default=' ', max_length=255, verbose_name='\u59d3\u540d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signorder',
            name='note',
            field=models.CharField(max_length=255, null=True, verbose_name='\u5907\u6ce8'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='signorder',
            name='phone',
            field=models.CharField(max_length=255, null=True, verbose_name='\u624b\u673a\u53f7\u7801'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='signorder',
            name='update_time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 30), auto_now=True),
            preserve_default=False,
        ),
    ]
