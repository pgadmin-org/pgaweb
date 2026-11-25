from django.db import migrations

# Since pgAdmin 6.12 the desktop application has used the operating
# system's file dialogues (FileManagerModule.showNative() in pgadmin4), so
# the FAQ claiming it never does is out of date. Only the original wording is
# replaced, so an answer that has since been edited by hand is left alone.
OLD_QUESTION = "Why doesn't pgAdmin use the native File management dialogues?"
OLD_MARKER = ('have consistently found that using our own dialogues provides '
              'the best experience')

NEW_QUESTION = "Why doesn't pgAdmin use native file dialogues in the browser?"
NEW_ANSWER = """<p>In the desktop application it does: since pgAdmin 6.12, opening and saving
files uses your operating system's own file dialogues. When pgAdmin runs in a
web browser it uses its own file manager instead, for a couple of reasons:</p>

<ul>
  <li>A web application can only interact with the local filesystem in the ways
  that modern web browsers allow, which for security reasons largely means
  "downloading" or "uploading" files. There is no way to simply save an update to
  a file by hitting a Save button, nor to remember the working directory.</li>
  <li>In server mode, files are read from and stored on the server, so that users
  can work with the same files whichever machine they happen to be using. There
  are no native dialogues for working with files stored on a web server in this
  way, so pgAdmin provides its own.</li>
</ul>"""


def update_faq(apps, schema_editor):
    Faq = apps.get_model('faq', 'Faq')

    # save() rather than update(), so that the post_save handler bans the
    # FAQ page from Varnish.
    for faq in Faq.objects.filter(question=OLD_QUESTION,
                                  answer__contains=OLD_MARKER):
        faq.question = NEW_QUESTION
        faq.answer = NEW_ANSWER
        faq.save()


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_features_screenshots_wording'),
    ]

    operations = [
        migrations.RunPython(update_faq,
                             reverse_code=migrations.RunPython.noop),
    ]
