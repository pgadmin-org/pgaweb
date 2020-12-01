##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render

from news.models import News


# Handle the root level pages
def index(request):
    news = News.objects.filter(disable=False)
    return render(request, 'news/news.html',
                  {'news': news})