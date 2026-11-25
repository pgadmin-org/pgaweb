from django.db import migrations

# pgAgent is no longer supported or maintained, so its download pages are
# retired. Hiding the package alone leaves each distribution's page live at
# /download/<slug>/, so the distributions are hidden too. Versions are left
# alone, as the documentation for older releases still refers to them.


def retire_pgagent(apps, schema_editor):
    Package = apps.get_model('download', 'Package')
    Distribution = apps.get_model('download', 'Distribution')

    # save() rather than update(), so that the post_save handler bans the
    # affected pages from Varnish.
    for package in Package.objects.filter(name__iexact='pgagent'):
        if package.active:
            package.active = False
            package.save()

        for distribution in Distribution.objects.filter(package=package,
                                                        active=True):
            distribution.active = False
            distribution.save()


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0012_alter_download_version'),
    ]

    operations = [
        migrations.RunPython(retire_pgagent,
                             reverse_code=migrations.RunPython.noop),
    ]
