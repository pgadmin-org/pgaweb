# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-04 10:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True)),
                ('active', models.BooleanField()),
                ('description', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('maintainer', models.CharField(max_length=100)),
                ('icon', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('order', 'package', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('download_url', models.CharField(max_length=250)),
                ('notes_url', models.CharField(blank=True, max_length=250)),
                ('distribution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='download.Distribution')),
            ],
            options={
                'ordering': ('version', 'distribution'),
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField()),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField()),
                ('released', models.DateField(default=datetime.date.today)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='download.Package')),
            ],
            options={
                'ordering': ('-released', 'name'),
            },
        ),
        migrations.AddField(
            model_name='download',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='download.Version'),
        ),
        migrations.AddField(
            model_name='distribution',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='download.Package'),
        ),
    ]