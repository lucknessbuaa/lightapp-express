# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField(default=0)),
                ('gender', models.IntegerField(default=0, verbose_name='\u6027\u522b', choices=[(1, '\u7537'), (0, '\u5973')])),
                ('name', models.CharField(max_length=255, verbose_name='\u59d3\u540d')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='\u5bbf\u820d\u5730\u5740')),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='SendOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('express', models.IntegerField(verbose_name='\u5feb\u9012\u516c\u53f8', choices=[(6, '\u767e\u4e16\u6c47\u901a'), (5, '\u987a\u4e30')])),
                ('time', models.DateTimeField(verbose_name='\u4e0a\u95e8\u65e5\u671f')),
                ('period', models.CharField(max_length=255, verbose_name='\u6536\u4ef6\u65f6\u95f4')),
                ('note', models.CharField(max_length=255, null=True, verbose_name='\u5907\u6ce8')),
                ('name', models.CharField(max_length=255, verbose_name='\u59d3\u540d')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='\u5bbf\u820d\u5730\u5740')),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('status', models.IntegerField(default=0, verbose_name='\u72b6\u6001', choices=[(0, '\u5904\u7406\u4e2d'), (1, '\u5df2\u6536\u4ef6\uff0c\u5f85\u5bc4\u51fa'), (2, '\u5df2\u5b8c\u6210'), (3, '\u8ba2\u5355\u53d6\u6d88')])),
                ('order_no', models.CharField(max_length=255, null=True, verbose_name='\u5feb\u9012\u5355\u53f7')),
                ('price', models.FloatField(null=True, verbose_name='\u4ef7\u683c')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='backend.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u59d3\u540d')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='\u5bbf\u820d\u5730\u5740')),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('express', models.IntegerField(verbose_name='\u5feb\u9012\u516c\u53f8', choices=[(1, '\u5706\u901a'), (2, '\u4e2d\u901a'), (3, '\u7533\u901a'), (4, '\u97f5\u8fbe'), (5, '\u987a\u4e30'), (6, '\u767e\u4e16\u6c47\u901a'), (7, 'EMS'), (8, '\u5929\u5929'), (9, '\u665f\u90a6'), (10, '\u4e9a\u9a6c\u900a'), (12, '\u552f\u54c1\u4f1a'), (13, '\u4e2d\u56fd\u90ae\u653f'), (16, '\u4eac\u4e1c'), (100, '\u5176\u5b83\u516c\u53f8')])),
                ('note', models.CharField(max_length=255, null=True, verbose_name='\u5907\u6ce8')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='backend.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoreItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StormItemOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField()),
                ('account', models.ForeignKey(to='backend.Account')),
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
