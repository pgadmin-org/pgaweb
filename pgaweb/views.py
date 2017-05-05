##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render_to_response
from django.template import RequestContext

from news.models import News
import pprint

# Handle the root level pages
def index(request):
    news = News.objects.filter(display=True)
    return render_to_response('pgaweb/index.html', {'news': news})


def contributing(request):
    return render_to_response('pgaweb/contributing.html', {})


def docs(request):
    return render_to_response('pgaweb/docs.html', {})


def features(request):
    return render_to_response('pgaweb/features.html', {})


def licence(request):
    return render_to_response('pgaweb/licence.html', {})


def privacy_policy(request):
    return render_to_response('pgaweb/privacy_policy.html', {})


def screenshots(request):
    return render_to_response('pgaweb/screenshots.html', {})


# Handle the Development level pages
def development_index(request):
    return render_to_response('pgaweb/development/index.html', {})


def development_resources(request):
    return render_to_response('pgaweb/development/resources.html', {})


def development_team(request):
    return render_to_response('pgaweb/development/team.html', {})


# Handle the Support level pages
def support_index(request):
    return render_to_response('pgaweb/support/index.html', {})


def support_issues(request):
    return render_to_response('pgaweb/support/issues.html', {})


def support_list(request):
    return render_to_response('pgaweb/support/list.html', {})


# Error handlers
def bad_request(request):
    response = render_to_response('pgaweb/errors/400.html')
    response.status_code = 400

    return response


def permission_denied(request):
    response = render_to_response('pgaweb/errors/403.html', {'path': request.path})
    response.status_code = 403

    return response


def page_not_found(request):
    response = render_to_response('pgaweb/errors/404.html', {'path': request.path})
    response.status_code = 404

    return response


def server_error(request):
    response = render_to_response('pgaweb/errors/500.html', { })
    response.status_code = 500

    return response
