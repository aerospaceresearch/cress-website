# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0008_action_cycle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(choices=[('DHT22', 'DHT22'), ('photoresistor', 'photoresistor'), ('photodiode', 'photodiode'), ('FC28', 'FC28')], max_length=100),
        ),
    ]
