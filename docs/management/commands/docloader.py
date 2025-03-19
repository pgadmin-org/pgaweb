##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from bs4 import BeautifulSoup
import glob
import os
from django.core.management.base import BaseCommand, CommandError
from docs.models import Page
from download.models import Package, Version
from django.db.utils import IntegrityError
from django.db.transaction import set_autocommit, commit, rollback
from pgaweb.settings import STATIC_URL


class Command(BaseCommand):
    help = 'Load HTML docs from a directory into the database.'

    def add_arguments(self, parser):
        parser.add_argument('package', help="the slug of the Package to link "
                                            "the document to.")

        parser.add_argument('version', help="the version number of the "
                                            "package to link the document to. "
                                            "Any text including and following "
                                            "the first non-numeric or . will "
                                            "be treated as the suffix.")

        parser.add_argument('source', help="the path to the directory "
                                           "containing the HTML files to load "
                                           "and index. Must be relative to "
                                           "$INSTDIR/static/docs")

    def load_docs(self, directory, static, version):
        """
        Load document pages from the given directory into the Document

        :param directory: The directory to load pages from
        :param static: The path to static files
        :param version: The Version object to load Pages into
        :return: The number of Pages loaded
        """

        count = 0
        path = os.path.join(directory, '**/*.htm*')

        for file in glob.iglob(path, recursive=True):
            self.stdout.write("Loading: {} ".format(file))

            f = open(file, 'r')
            html = f.read()
            f.close()

            # Get the filename
            filename = file.replace(directory, '')
            if filename.startswith('/'):
                filename = filename[1:]

            static_dir = os.path.join(STATIC_URL, static)
            if '/' in filename:
                static_dir = os.path.join(STATIC_URL, static,
                                          filename[0:filename.rfind('/')])

            # Extract the HTML
            soup = BeautifulSoup(html, features="html.parser")

            # Update paths to images
            for img in soup.findAll('img'):
                img['src'] = os.path.join(static_dir, img['src'])

            for obj in soup.findAll('object'):
                if obj.has_attr('data'):
                    obj['data'] = os.path.join(static_dir, obj['data'])
                if obj.has_attr('width'):
                    del obj['width']

            # Remove the search box if present
            for div in soup.findAll('div'):
                if div.has_attr('id') and div['id'] == 'searchbox':
                    div.extract()
            for search in soup.findAll('search'):
                if search.has_attr('id') and search['id'] == 'searchbox':
                    search.extract()

            # If there's no title, use the filename (without the .html)
            if soup.find('title') is not None:
                title = soup.find('title').decode_contents(formatter="html").strip()
            else:
                title = filename[:-5]

            # Remove the title, as we no longer need it
            [x.extract() for x in soup.find_all('title')]

            # Get the page header navigation
            header = soup.find('div', role='navigation').decode_contents(formatter="html").strip()

            # Get the contents panel
            contents_soup = soup.find('div', class_='sphinxsidebarwrapper')
            [x.extract() for x in contents_soup.find_all('h3')]
            contents = contents_soup.decode_contents(formatter="html").strip()

            # Get the page content
            body = soup.find('div', class_='body').decode_contents(formatter="html").strip()

            # We want the Contents header to be an H1 not H2
            contents = contents.replace('h3>', 'h1>')

            # Create the new Page
            try:
                page = Page.objects.create(version=version, file=filename,
                                           title=title, header=header,
                                           contents=contents, body=body)
            except IntegrityError as e:
                rollback()
                raise CommandError("Rolling back: failed to insert {}: {}".
                                   format(filename, str(e)))

            page.save()

            count = count + 1

        return count

    def handle(self, *args, **options):
        """The core structure of the app."""

        # Get the various paths we need
        root_dir = os.path.realpath(os.path.join(
            os.path.dirname(__file__), '../../../'))

        source_path = os.path.join(root_dir, 'static/docs', options['source'])

        static_dir = os.path.join('docs', options['source'])
        if os.path.isfile(source_path):
            static_dir = os.path.dirname(os.path.join('docs',
                                                      options['source']))

        # Disable autocommit so this all runs in a transaction
        set_autocommit(False)

        # Check the Package exists
        package = Package.objects.filter(slug=options['package']).first()

        if package is None:
            raise CommandError("The Package object could not be found.")

        # Check the Version exists
        version = Version.objects.filter(name=options['version'],
                                         package=package).first()

        if version is None:
            raise CommandError("The Version object could not be found.")

        # Delete all existing pages and load the new ones from the dir
        Page.objects.filter(version_id=version.id).delete()

        count = self.load_docs(source_path,
                               static_dir,
                               version)

        commit()

        self.stdout.write("Loaded {} pages into {}".format(
            count, str(version)))
