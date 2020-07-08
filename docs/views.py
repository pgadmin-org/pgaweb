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
    canonical = False
    latest = Version.objects.filter(active=True,
                                     released__isnull=False,
                                     package__slug=package,
                                     page__isnull=False).first()

    if latest is None:
        raise Http404("The requested page could not be found.")

    if version and version == 'latest':
        canonical = True
        version = latest.slug

    # Get all pages, so we can build the "other versions" links
    pages = Page.objects.filter(file=file,
                                version__package__slug=package,
                                version__active=True,
                                version__package__active=True)

    # Grab the required version of the page for rendering, and check to see
    # if we should show the "latest version" link.
    show_latest = False
    page = None
    for p in pages:
        if p.version.slug == latest.slug:
            show_latest = True
        if p.version.slug == version:
            page = p

    if page is None:
        raise Http404("The requested page could not be found.")

    data = {'page': page, 'pages': pages, 'show_latest': show_latest}

    response = render(request, 'docs/page.html', data)

    # 'latest' version links should be canonical
    if canonical:
        response['rel'] = 'canonical'

    return response
