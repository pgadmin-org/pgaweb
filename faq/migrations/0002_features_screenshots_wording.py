from django.db import migrations

# The screenshots page was merged into the features page, so the FAQ no
# longer has a separate Screenshots page to point at.
OLD = ('please see the <a href="/features/">Features</a> and '
       '<a href="/screenshots/">Screenshots</a> pages.')
NEW = ('please see the <a href="/features/">Features</a> page, which '
       'includes <a href="/features/#screenshots">screenshots</a>.')


def update_answers(apps, schema_editor):
    Faq = apps.get_model('faq', 'Faq')

    # save() rather than update(), so that the post_save handler bans the
    # FAQ page from Varnish.
    for faq in Faq.objects.filter(answer__contains=OLD):
        faq.answer = faq.answer.replace(OLD, NEW)
        faq.save()


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_answers,
                             reverse_code=migrations.RunPython.noop),
    ]
