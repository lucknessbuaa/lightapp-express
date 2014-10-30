# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20141030_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendorder',
            name='address',
            field=models.CharField(default=' ', max_length=255, verbose_name='\u5730\u5740'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='create_time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 30), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='express',
            field=models.IntegerField(default=6, verbose_name='\u5feb\u9012\u516c\u53f8', choices=[(6, '\u767e\u4e16\u6c47\u901a'), (5, '\u987a\u4e30')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='name',
            field=models.CharField(default=' ', max_length=255, verbose_name='\u59d3\u540d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='note',
            field=models.CharField(max_length=255, null=True, verbose_name='\u5907\u6ce8'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='phone',
            field=models.CharField(default=' ', max_length=255, verbose_name='\u7535\u8bdd'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='update_time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 30), auto_now=True),
            preserve_default=False,
        ),
    ]
