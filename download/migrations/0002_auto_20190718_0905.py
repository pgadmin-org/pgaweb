# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-18 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='slug',
            field=models.SlugField(blank=True, help_text=b'The string to use to identify this item in URLs. Leave blank to auto-generate.', max_length=100),
        ),
    ]
