##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.search, name='search'),
    re_path(r'^versions/$', views.versions, name='versions'),
]
