##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.http import HttpResponse
from django.shortcuts import render

from news.models import News
from versions.models import Version


# Handle the root level pages
def index(request):
    news = News.objects.filter(display=True)
    version = Version.objects.get(package='pgadmin4', active=True)
    return render(request, 'pgaweb/index.html',
                  {'news': news, 'version': version})


def ads_txt(request):
    return HttpResponse(
        "google.com, pub-7509009547019933, DIRECT, f08c47fec0942fa0")


def contributing(request):
    return render(request, 'pgaweb/contributing.html', {})


def features(request):
    return render(request, 'pgaweb/features.html', {})


def licence(request):
    return render(request, 'pgaweb/licence.html', {})


def privacy_policy(request):
    return render(request, 'pgaweb/privacy_policy.html', {})


def screenshots(request):
    return render(request, 'pgaweb/screenshots.html', {})


def try_pgadmin(request):
    return render(request, 'pgaweb/try_pgadmin.html', {})


# Handle the Development level pages
def development_index(request):
    return render(request, 'pgaweb/development/index.html', {})


def development_resources(request):
    return render(request, 'pgaweb/development/resources.html', {})


def development_team(request):
    return render(request, 'pgaweb/development/team.html', {})


# Handle the Styleguide pages
def styleguide_index(request, page='typography', section=''):

    if page == 'themes' and not section:
        section = 'color'

    if page == 'iconography' and not section:
        section = 'fontawesome'

    return render(request, 'pgaweb/styleguide/index.html', {'page': page, 'section': section})

# Handle the Support level pages
def support_index(request):
    return render(request, 'pgaweb/support/index.html', {})


def support_issues(request):
    return render(request, 'pgaweb/support/issues.html', {})


def support_list(request):
    return render(request, 'pgaweb/support/list.html', {})


# Error handlers
def bad_request(request, exception):
    response = render(request, 'pgaweb/errors/400.html')
    response.status_code = 400

    return response


def permission_denied(request, exception):
    response = render(request, 'pgaweb/errors/403.html', {'path': request.path})
    response.status_code = 403

    return response


def page_not_found(request, exception):
    response = render(request, 'pgaweb/errors/404.html', {'path': request.path})
    response.status_code = 404

    return response


def server_error(request):
    response = render(request, 'pgaweb/errors/500.html', { })
    response.status_code = 500

    return response
