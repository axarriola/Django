# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mplsbgp', '0002_junosdevice_logical_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='junosdevice',
            name='logical_system',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
