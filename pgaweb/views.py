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

import glob
import os
import ast
from babel.messages.pofile import read_po

from pgaweb import settings

from news.models import News
from versions.models import Version
from blogs.models import Blog
from videos.models import Video


# Handle the root level pages
def index(request):
    news = News.objects.filter(display=True, disable=False)
    version = Version.objects.get(package='pgadmin4', active=True)
    blogs = Blog.objects.filter(disable=False, display=True)[:3]
    videos = Video.objects.filter(disable=False, display=True)[:3]
    return render(request, 'pgaweb/index.html',
                  {'news': news, 'version': version,
                   'blogs': blogs, 'videos': videos})


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


# Handle the Development level pages
def development_index(request):
    return render(request, 'pgaweb/development/index.html', {})


def development_resources(request):
    return render(request, 'pgaweb/development/resources.html', {})


def development_team(request):
    return render(request, 'pgaweb/development/team.html', {})


def development_translations(request):
    base_path = os.path.join(settings.PGADMIN_TREE_PATH, 'web', 'pgadmin')

    # Get the list of languages from pgAdmin
    languages = '{\n'
    with open(os.path.join(settings.PGADMIN_TREE_PATH, 'web', 'config.py'), 'r') as f:
        lines = f.readlines()
        started = False
        for line in lines:
            if started:
                if line[:1] == '}':
                    break
                else:
                    languages = languages + line.replace('\'', '"')
            else:
                if line[:13] == 'LANGUAGES = {':
                    started = True
    languages = ast.literal_eval(languages + '}')

    with open(os.path.join(base_path, 'messages.pot'), 'r') as t:
        catalog = read_po(t)
        total_messages = len(catalog)

    context = {'total_messages': total_messages}
    catalogs = []

    for po in glob.iglob(os.path.join(base_path,
                                      'translations/*/LC_MESSAGES/messages.po')):

        catalog = {}

        with open(po, 'r') as p:
            c = read_po(p)

            fuzzy = sum(x.fuzzy is True for x in c)
            untranslated = sum(x.string == '' for x in c)

            catalog['file'] = po[len(base_path) + 14:]
            catalog['language'] = languages[po[len(base_path) + 14:][:2]]
            catalog['revised'] = c.revision_date.strftime("%Y-%m-%d")
            catalog['translator'] = ' '.join([i for i in c.last_translator.split() if '@' not in i])
            catalog['total_messages'] = len(c)
            catalog['total_messages_pct'] = 100 / total_messages * catalog['total_messages']
            catalog['translated_messages'] = catalog['total_messages'] - untranslated
            catalog['translated_messages_pct'] = 100 / catalog['total_messages'] * catalog['translated_messages']
            catalog['status_icon'] = '<i class="fa fa-question-circle text-warning" aria-hidden="true">'
            if catalog['translated_messages_pct'] >= 95:
                catalog['status_icon'] = '<i class="fa fa-check-circle text-success" aria-hidden="true">'
            elif catalog['translated_messages_pct'] < 75:
                catalog['status_icon'] = '<i class="fa fa-exclamation-circle text-danger" aria-hidden="true">'
            catalog['fuzzy_messages'] = fuzzy
            catalog['fuzzy_messages_pct'] = 100 / catalog['total_messages'] * catalog['fuzzy_messages']
            catalog['untranslated_messages'] = untranslated
            catalog['untranslated_messages_pct'] = 100 / catalog['total_messages'] * catalog['untranslated_messages']

        catalogs.append(catalog)

    context['catalogs'] = sorted(catalogs, key=lambda k: k['language'])

    return render(request, 'pgaweb/development/translations.html', context)


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
