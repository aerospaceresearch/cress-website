# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0010_auto_20160508_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='purged',
            field=models.BooleanField(default=False),
        ),
    ]
