# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databasework', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepos', models.FileField(upload_to='./upload/')),
                ('upload_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'excel_file',
            },
        ),
        migrations.AlterModelTable(
            name='basestation',
            table='base_station',
        ),
    ]