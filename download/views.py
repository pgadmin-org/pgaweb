##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import get_object_or_404, render_to_response

from download.models import Distribution, Download, Package


# Handle the Download pages
def index(request):
    packages = Package.objects.filter(active=True)
    return render_to_response('download/index.html', {'packages': packages})


def download_list(request, slug):
    distribution = get_object_or_404(Distribution, slug=slug, active=True)
    distributions = Distribution.objects.filter(package=distribution.package, active=True).exclude(id=distribution.id)
    downloads = Download.objects.filter(distribution=distribution, active=True)

    return render_to_response('download/distribution.html', {'distribution': distribution,
                                                             'distributions': distributions,
                                                             'downloads': downloads})
