# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20141030_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendorder',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='\u5bbf\u820d\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='\u59d3\u540d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='phone',
            field=models.CharField(max_length=255, null=True, verbose_name='\u624b\u673a\u53f7\u7801'),
            preserve_default=True,
        ),
    ]
