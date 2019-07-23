from __future__ import unicode_literals

from django.db import migrations, models
from django.template.defaultfilters import slugify


def update_slugs(apps, schema_editor):
    Package = apps.get_model("download", "Package")

    for instance in Package.objects.all():
        instance.slug = slugify(instance.name)
        instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_auto_20190718_0905'),
    ]

    operations = [
        migrations.RunPython(update_slugs,
                             reverse_code=migrations.RunPython.noop),
    ]
