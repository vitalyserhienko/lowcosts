# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricetype',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
