# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-13 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_auto_20160513_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsable',
            name='hash_id',
            field=models.CharField(default=None, max_length=200),
        ),
    ]