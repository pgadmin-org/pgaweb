##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityAdvisory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osv_id', models.CharField(max_length=64, unique=True)),
                ('cve_id', models.CharField(blank=True, max_length=32)),
                ('summary', models.CharField(blank=True, max_length=512)),
                ('details', models.TextField(blank=True)),
                ('cvss_vector', models.CharField(blank=True, max_length=128)),
                ('base_score', models.FloatField(blank=True, null=True)),
                ('severity', models.CharField(blank=True, max_length=16)),
                ('affected_ranges', models.JSONField(blank=True, default=list)),
                ('fixed_versions', models.JSONField(blank=True, default=list)),
                ('references', models.JSONField(blank=True, default=list)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('osv_url', models.URLField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('suppressed', models.BooleanField(default=False)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Security Advisory',
                'verbose_name_plural': 'Security Advisories',
                'ordering': ('-base_score', '-published'),
            },
        ),
    ]
