##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render_to_response

from versions.models import Version


# Handle the static pages
def versions(request):
    versions = Version.objects.filter(active=True)
    return render_to_response('versions/versions.json', {'versions': versions})

