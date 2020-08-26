##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.template.exceptions import TemplateDoesNotExist

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
def styleguide_redirect(request):
    return redirect('styleguide_index', page='typography')


def styleguide_index(request, page='typography', section=''):
    # Iconography section
    if page == 'iconography':
        section = 'fontawesome' if not section else section

        # Check for a valid section
        if section not in ['fontawesome',
                           'custom_icons',
                           'tree_view_icons',
                           'query_plans']:
            raise Http404("The requested page could not be found.")

        template = 'pgaweb/styleguide/{0}/{0}.html'.format(page)

    # Themes section
    elif page == 'themes':
        section = 'color_palettes' if not section else section

        if section not in ['accordions',
                           'alerts',
                           'buttons',
                           'checkboxes',
                           'color_palettes',
                           'dropdowns',
                           'input_fields',
                           'menus',
                           'radio_buttons',
                           'tab_sets',
                           'tables',
                           'toggle_buttons']:
            raise Http404("The requested page could not be found.")

        template = 'pgaweb/styleguide/{0}/{1}.html'.format(section, section)

    # Other pages
    else:
        template = 'pgaweb/styleguide/{0}.html'.format(page)

    try:
        response = render(request, template, {'page': page, 'section': section})
    except TemplateDoesNotExist as e:
        raise Http404("The requested page could not be found.")

    return response


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
