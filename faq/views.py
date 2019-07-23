##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.shortcuts import render

from faq.models import Faq


# Handle the various pages
def index(request):
    faqs = Faq.objects.filter(active=True)

    return render(request, 'faq/faq.html', {'faqs': faqs})
