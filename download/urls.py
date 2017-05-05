##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'download.views.index', name='download_index'),
    url(r'^(?P<slug>[\w-]+)$', 'download.views.download_list', name='download_list'),
]
