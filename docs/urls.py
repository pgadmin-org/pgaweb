##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.urls import re_path
from docs import views as docs_views

urlpatterns = [
    re_path(r'^$', docs_views.docs, name='docs'),
    re_path(r'^([^/]+)/([^/]+)/$', docs_views.page, name='page'),
    re_path(r'^([^/]+)/([^/]+)/(.+)$', docs_views.page, name='page'),
]
