##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render_to_response

from news.models import News


# Handle the various pages
def index(request):
    news = News.objects.filter(display=True)
    return render_to_response('pgaweb/index.html', {'news': news})


def contributing(request):
    return render_to_response('pgaweb/contributing.html', {})


def features(request):
    return render_to_response('pgaweb/features.html', {})


def licence(request):
    return render_to_response('pgaweb/licence.html', {})


def privacy_policy(request):
    return render_to_response('pgaweb/privacy_policy.html', {})