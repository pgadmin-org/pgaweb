##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.urls import re_path
from download import views as download_views

urlpatterns = [
    re_path(r'^$', download_views.index, name='download_index'),
    re_path(r'^(?P<slug>[\w-]+)/$', download_views.download_list, name='download_list'),
]
