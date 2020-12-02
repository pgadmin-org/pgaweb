##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render

from videos.models import Video


# Handle the root level pages
def index(request):
    videos = Video.objects.filter(disable=False)
    return render(request, 'videos/videos.html',
                  {'videos': videos})