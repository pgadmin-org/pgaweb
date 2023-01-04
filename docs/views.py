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
from download.models import Version
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
        if pages.count() == 0:
            raise Http404("The requested page could not be found.")

        # Return a custom 404 page, with suggested additional pages
        # First, get the max lengths of the version and title
        version_max = 7  # Length of "version"
        title_max = 5  # Length of "title"
        for p in pages:
            if len(p.version.name) > version_max:
                version_max = len(p.version.name)
            if len(p.title) > title_max:
                title_max = len(p.title)

        data = {'path': request.path,
                'pages': pages,
                'version_l_pad': version_max + 2,
                'version_t_pad': version_max - 6,
                'version_v_pad': version_max + 1,
                'title_l_pad': title_max - 4,
                'title_t_pad': title_max / 2 - 5}
        response = render(request, 'docs/404.html', data)
        response.status_code = 404

        return response

    data = {'page': page, 'pages': pages, 'show_latest': show_latest}

    response = render(request, 'docs/page.html', data)

    # 'latest' version links should be canonical
    if canonical:
        response['rel'] = 'canonical'

    return response
