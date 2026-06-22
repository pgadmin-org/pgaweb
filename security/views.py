##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.db.models import F, Max
from django.shortcuts import render

from security.models import SecurityAdvisory


def index(request):
    # Show the most recently published advisories first. Any advisory without a
    # published date sorts last, with the identifier as a stable tiebreaker.
    advisories = (SecurityAdvisory.objects.filter(suppressed=False)
                  .order_by(F('published').desc(nulls_last=True), '-cve_id'))

    last_updated = advisories.aggregate(Max('last_seen'))['last_seen__max']

    return render(request, 'security/security.html',
                  {'advisories': advisories, 'last_updated': last_updated})
