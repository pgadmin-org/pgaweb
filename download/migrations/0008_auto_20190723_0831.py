from __future__ import unicode_literals

from django.db import migrations

from download.models import version_slugify


def update_slugs(apps, schema_editor):
    Version = apps.get_model("download", "Version")

    for instance in Version.objects.all():
        instance.slug = version_slugify(instance.name)
        instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0007_auto_20190723_0830'),
    ]

    operations = [
        migrations.RunPython(update_slugs,
                             reverse_code=migrations.RunPython.noop),
    ]
