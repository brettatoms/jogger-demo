# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170709_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jog',
            name='date',
            field=models.DateField(),
        ),
    ]
