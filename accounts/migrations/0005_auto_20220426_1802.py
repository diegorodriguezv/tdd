# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-04-26 18:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220424_0522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='id',
        ),
        migrations.AlterField(
            model_name='token',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=40, primary_key=True, serialize=False),
        ),
    ]
