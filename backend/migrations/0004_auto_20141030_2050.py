# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20141030_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendorder',
            name='address',
        ),
        migrations.RemoveField(
            model_name='sendorder',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sendorder',
            name='phone',
        ),
        migrations.AddField(
            model_name='sendorder',
            name='period',
            field=models.CharField(default='20:00-21:00', max_length=255, verbose_name='\u6536\u4ef6\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 30), verbose_name='\u4e0a\u95e8\u65e5\u671f'),
            preserve_default=False,
        ),
    ]
