# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20141104_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendorder',
            name='order_no',
            field=models.CharField(max_length=255, null=True, verbose_name='\u5feb\u9012\u5355\u53f7'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='price',
            field=models.FloatField(null=True, verbose_name='\u4ef7\u683c'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='status',
            field=models.IntegerField(default=0, verbose_name='\u72b6\u6001', choices=[(0, '\u672a\u5904\u7406'), (1, '\u5df2\u6536\u4ef6'), (2, '\u5df2\u5bc4\u51fa'), (3, '\u8ba2\u5355\u53d6\u6d88')]),
            preserve_default=True,
        ),
    ]
