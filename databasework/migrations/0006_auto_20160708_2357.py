# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databasework', '0005_auto_20160708_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms',
            name='imei',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
    ]
