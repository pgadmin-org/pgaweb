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


# Handle the static pages
def index(request):
    news = News.objects.filter(display=True)
    return render_to_response('index.html', {'news': news})

