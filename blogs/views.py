##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render

from blogs.models import Blog


# Handle the root level pages
def index(request):
    blogs = Blog.objects.filter(disable=False)
    return render(request, 'blogs/blogs.html',
                  {'blogs': blogs})