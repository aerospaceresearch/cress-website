# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0029_auto_20170617_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='soil',
            field=models.CharField(blank=True, choices=[('cotton wool (medical)', 'cotton wool (medical)'), ('cotton wool (cosmetics)', 'cotton wool (cosmetics)'), ('red clay (Seramis)', 'red clay (Seramis)'), ('orchid soil (Orchideenerde)', 'orchid soil (Orchideenerde)'), ('potting soil', 'potting soil')], max_length=255, null=True),
        ),
    ]
