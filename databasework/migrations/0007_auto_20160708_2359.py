# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databasework', '0006_auto_20160708_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms',
            name='mzone',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
