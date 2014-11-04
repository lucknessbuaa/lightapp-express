# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20141030_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(verbose_name='\u8d2d\u4e70\u6570\u91cf')),
                ('name', models.CharField(max_length=255, verbose_name='\u6536\u4ef6\u4eba\u59d3\u540d')),
                ('phone', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7')),
                ('destination', models.CharField(max_length=255, verbose_name='\u6536\u4ef6\u5730\u5740')),
                ('notes', models.CharField(max_length=255, verbose_name='\u5907\u6ce8')),
                ('status', models.IntegerField(verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('total_price', models.IntegerField()),
                ('total_points', models.IntegerField()),
                ('account', models.ForeignKey(to='backend.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goodsid', models.IntegerField(default=0, verbose_name='\u5546\u54c1id')),
                ('name', models.CharField(max_length=255, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('description', models.CharField(max_length=255, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('detailinfo', models.CharField(max_length=500, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbf\xa1\xe6\x81\xaf')),
                ('rating', models.IntegerField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x8e\xa8\xe8\x8d\x90\xe6\x98\x9f\xe7\xba\xa7', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('thumburl', models.CharField(max_length=255, verbose_name=b'\xe5\xb0\x8f\xe5\x9b\xbe\xe6\xa0\x87')),
                ('imgurl', models.CharField(max_length=255, verbose_name=b'\xe5\xa4\xa7\xe5\x9b\xbe\xe6\xa0\x87')),
                ('price', models.IntegerField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc')),
                ('points', models.IntegerField(verbose_name=b'\xe6\x89\x80\xe9\x9c\x80\xe7\xa7\xaf\xe5\x88\x86')),
                ('num', models.IntegerField(verbose_name=b'\xe6\x80\xbb\xe9\x87\x8f')),
                ('consumption', models.IntegerField(verbose_name=b'\xe5\xb7\xb2\xe5\x87\xba\xe5\x94\xae\xe6\x95\xb0\xe9\x87\x8f')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goodorder',
            name='goods',
            field=models.ForeignKey(to='backend.Goods'),
            preserve_default=True,
        ),
    ]
