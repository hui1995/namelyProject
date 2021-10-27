# Generated by Django 2.2 on 2021-03-08 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_auto_20210308_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='c_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 17, 21, 29, 720287)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='g_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 17, 21, 29, 721288)),
        ),
        migrations.AlterField(
            model_name='public',
            name='p_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 17, 21, 29, 720287)),
        ),
        migrations.AlterField(
            model_name='repair',
            name='r_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 17, 21, 29, 720287)),
        ),
        migrations.AlterField(
            model_name='report',
            name='feedback',
            field=models.CharField(blank=True, default='', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 17, 21, 29, 721288)),
        ),
    ]
