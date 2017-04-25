##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render_to_response

from faq.models import Faq


# Handle the various pages
def index(request):
    faqs = Faq.objects.filter(active=True)

    return render_to_response('faq/faq.html', {'faqs': faqs})
