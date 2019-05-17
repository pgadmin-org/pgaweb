##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.http import JsonResponse

from versions.models import Version


# The version list used for upgrade checks.
def index(request):
    versions = list(Version.objects.filter(active=True).values())

    json = {}
    for version in versions:
        data = {'version': version['version_str'],
                'version_int': version['version_int'],
                'download_url': version['download_url']}
        json[version['package']] = data

    return JsonResponse(json, json_dumps_params={'indent': 1})

