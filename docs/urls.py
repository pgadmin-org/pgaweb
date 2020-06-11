##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.conf.urls import url
from docs import views as docs_views

urlpatterns = [
    url(r'^$', docs_views.docs, name='docs'),
    url(r'^([^/]+)/([^/]+)/$', docs_views.page, name='page'),
    url(r'^([^/]+)/([^/]+)/(.+)$', docs_views.page, name='page'),
]
