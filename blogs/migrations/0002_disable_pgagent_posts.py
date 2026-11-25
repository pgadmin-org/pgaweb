from django.db import migrations

# pgAgent is no longer supported or maintained, so posts about it are taken
# off the blogs page. Matched on the title rather than the summary, so that
# posts which only mention pgAgent in passing are left alone.


def disable_posts(apps, schema_editor):
    Blog = apps.get_model('blogs', 'Blog')

    # save() rather than update(), so that the post_save handler bans the
    # affected pages from Varnish.
    for blog in Blog.objects.filter(title__icontains='pgagent', disable=False):
        blog.disable = True
        blog.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(disable_posts,
                             reverse_code=migrations.RunPython.noop),
    ]
