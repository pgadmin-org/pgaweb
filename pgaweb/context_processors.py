##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################


from docs.models import Page


def get_docs(request):
    pages = Page.objects.filter(version__active=True,
                                version__package__active=True,
                                file='index.html')

    return {'docs': pages}