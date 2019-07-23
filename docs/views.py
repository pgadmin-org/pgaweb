##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
from download.models import Version, Package
from docs.models import Page


def docs(request):
    # Get the available doc versions
    pages = Page.objects.filter(version__active=True,
                                version__package__active=True,
                                file='index.html')

    data = {'pages': pages}

    return render(request, 'docs/docs.html', data)


def page(request, package, version, file='index.html'):
    """
    Display an documentation page from the database

    :param request: The request object.
    :param package: The slug for the requested package.
    :param version: The requested version number.
    :param page: The file name of the requested page.
    :return: The rendered document page.

    **Template:**

    :template:`docs/page.html`
    """
    # Find the latest version of the docs if requested
    if version and version == 'latest':
        version = Version.objects.filter(active=True,
                                         released__isnull=False,
                                         package__slug=package,
                                         page__isnull=False).first().slug

    pages = Page.objects.filter(file=file,
                                version__package__slug=package,
                                version__active=True,
                                version__package__active=True)

    for page in pages:
        if page.version.slug == version:
            break
        else:
            page = None

    if page is None:
        raise Http404("The requested page could not be found.")

    data = {'page': page, 'pages': pages}

    return render(request, 'docs/page.html', data)

