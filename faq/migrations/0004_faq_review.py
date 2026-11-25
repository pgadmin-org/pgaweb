from django.db import migrations

# A review of the FAQ against the pgAdmin 4 source and documentation as of
# pgAdmin 9.x. Each change is keyed on a phrase from the entry's original
# wording, so an entry that has since been edited by hand is left alone.

# Small corrections: (marker, old text, new text). The marker selects the
# entry; old text is replaced with new text within its answer.
REPLACE = [
    # The User Management page was renamed; the old name is a 404.
    ('/docs/pgadmin4/development/pgadmin_user.html',
     '/docs/pgadmin4/development/pgadmin_user.html',
     '/docs/pgadmin4/development/user_management.html'),

    # The Windows and macOS packages have bundled the utilities for years.
    ('Future versions of pgAdmin may include them in some desktop packages.',
     'Future versions of pgAdmin may include them in some desktop packages.',
     'The Windows and macOS packages of pgAdmin also include <i>pg_dump</i>, '
     '<i>pg_dumpall</i>, <i>pg_restore</i> and <i>psql</i>.'),

    # The server mode log location was missing.
    ('<li><b>Windows: </b>%APPDATA%\\pgAdmin\\pgadmin4.log</li>',
     '<li><b>Linux/MacOS: </b>~/.pgadmin/pgadmin4.log</li>',
     '<li><b>Linux/MacOS, desktop mode: </b>~/.pgadmin/pgadmin4.log</li>\r\n'
     '  <li><b>Linux/MacOS, server mode: </b>/var/log/pgadmin/pgadmin4.log'
     '</li>'),
]

# Rewrites: (marker, new question, new answer).
REWRITE = [
    # Version numbers went stale as soon as they were written.
    ('<li>Chrome 109+</li>',
     'What browsers does pgAdmin support?',
     """<p>pgAdmin supports current versions of Chrome, Firefox, Edge and Safari.
We regularly test with them, and aim to fix issues found with any of them.</p>

<p>Other browsers may work but are not tested, and issues reported when using
them with pgAdmin may not be fixed.</p>"""),

    # pgAdmin uses the operating system's password store since 7.2, and
    # disabling the Master Password removes saved passwords.
    ("Unfortunately this ability isn't limited to administrative users",
     'What is the Master Password, and how do I use it or remove it?',
     """<p>The <a href="/docs/pgadmin4/latest/master_password.html">Master Password</a>
is used to securely encrypt any credentials that you choose to save when using
pgAdmin. It is used in desktop mode, and in server mode when the authentication
source is OAuth2, Kerberos or Webserver.</p>

<p>Since pgAdmin 7.2, the desktop application stores saved passwords in the
operating system's password store by default, and no Master Password is
required. pgAdmin only falls back to the Master Password if the operating
system's password store is not available.</p>

<p>Without the Master Password (or something similar that is supplied by the
user), the encryption key must be derived from data that is stored on disk in a
location known to pgAdmin. Anyone, or any malware, able to read that data could
decrypt the saved passwords. The Master Password prevents this, because it is
<b>never</b> stored on disk.</p>

<p><i>Can I disable the Master Password?</i> Yes, though we <b>strongly</b>
advise against doing so! Find the <i>config.py</i> file that is part of your
pgAdmin installation, normally in a top-level directory called <i>web</i>. In the
same directory, create a file called <i>config_local.py</i> (or edit it, if it
already exists), and add a line that reads:</p>

<pre>MASTER_PASSWORD_REQUIRED = False</pre>

<p>When you restart pgAdmin, any passwords that were already saved will be
removed. Passwords saved from then on will be encrypted with a key derived from
information in the configuration database, which will protect them against
"shoulder surfing", but will not prevent anyone with access to that database
from decrypting them fairly easily.</p>

<p><i>But why can't I disable the Master Password from the GUI?</i> By requiring
a change to the main configuration for pgAdmin, we allow system administrators
to enforce a security policy, which is often a requirement in corporate or other
secure environments.</p>"""),

    # The refresh rates moved, and the desktop runtime now captures logs.
    ("weren't present in pgAdmin III",
     'Why does pgAdmin seem to use a lot of CPU cycles?',
     """<p>pgAdmin is a web application, even when run in desktop mode, so it will
naturally use more CPU and memory than a traditional native desktop application.
It also includes dashboards that continually poll the database server and update
their graphs every few seconds. CPU usage may be noticeably reduced by setting
longer refresh rates under <i>File -&gt; Preferences -&gt; Dashboards -&gt;
Refresh rates</i>.</p>"""),

    ('/usr/local/pgadmin4/bin/pgadmin4',
     'How do I see the console output from pgAdmin?',
     """<p>In desktop mode, the pgAdmin application captures the console output of
the pgAdmin server. To see it, choose <i>View Logs...</i> from the <i>File</i>
menu, or from the <i>pgAdmin 4</i> menu on macOS.</p>

<p>If you're running in server mode, or directly using Python, the console output
is sent to the terminal from which the application was started.</p>

<p>Note that you may need to adjust the CONSOLE_LOG_LEVEL option in
config_local.py to see useful information in the log. See this
<a href="#8">FAQ</a> for more information.</p>"""),

    # Written for macOS 10.10, whose settings no longer exist.
    ('older versions of macOS (e.g. 10.10)',
     'On macOS, I get an error like: "pgAdmin 4 is damaged and cannot be opened"',
     """<p>This usually means that the download was incomplete or corrupted. Delete
the application, then download and install a fresh copy from the
<a href="/download/">download</a> page.</p>

<p>If macOS instead reports that it cannot verify the application, open
<i>System Settings</i> and browse to <i>Privacy &amp; Security</i>, where you can
choose to open it anyway. The available options and their labels vary from
release to release of macOS, and may not be exactly as described here.</p>"""),

    # Merged with the v4.28 loading page entry, which has the same cause.
    ('ignoring the stylesheets that properly format the display',
     'On Windows, pgAdmin never finishes loading, or I just see unformatted '
     'text. Why?',
     """<p>pgAdmin tells the browser to trust only the declared content type of each
file it serves, to prevent security issues caused by
<a href="https://en.wikipedia.org/wiki/Content_sniffing">content sniffing</a>.
On Windows, those content types are read from the registry, and some
applications set them to incorrect values. When that happens, the browser
refuses to use pgAdmin's JavaScript or stylesheets, and opening the developer
tools will show an error saying that a script or stylesheet was refused because
of its MIME type.</p>

<p>To resolve the issue, use the Registry Editor to check the following values,
correct any that are wrong, and then restart pgAdmin:</p>

<ul>
  <li><b>HKEY_CLASSES_ROOT\\.js\\Content Type</b> should be <b>text/javascript</b></li>
  <li><b>HKEY_CLASSES_ROOT\\.css\\Content Type</b> should be <b>text/css</b></li>
</ul>"""),
]

# Entries to remove, by marker.
DELETE = [
    # Merged into the Windows entry above.
    'pgAdmin 4 v4.28 includes additional security features',
    # A Safari 12 bug; pgAdmin now supports only current Safari, and no
    # longer defaults to SameSite=None.
    'CFNetwork/Webkit',
]


def update_faqs(apps, schema_editor):
    Faq = apps.get_model('faq', 'Faq')

    # save() rather than update(), so that the post_save handler bans the
    # FAQ page from Varnish. There is no post_delete handler, but the saves
    # in this same migration ban the page anyway.
    for marker, old, new in REPLACE:
        for faq in Faq.objects.filter(answer__contains=marker):
            faq.answer = faq.answer.replace(old, new)
            faq.save()

    for marker, question, answer in REWRITE:
        for faq in Faq.objects.filter(answer__contains=marker):
            faq.question = question
            faq.answer = answer
            faq.save()

    for marker in DELETE:
        for faq in Faq.objects.filter(answer__contains=marker):
            faq.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_native_file_dialogues'),
    ]

    operations = [
        migrations.RunPython(update_faqs,
                             reverse_code=migrations.RunPython.noop),
    ]
