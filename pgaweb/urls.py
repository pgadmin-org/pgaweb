##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""pgaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'pgaweb.views.index', name='index'),
    url(r'^contributing$', 'pgaweb.views.contributing', name='contributing'),
    url(r'^features$', 'pgaweb.views.features', name='features'),
    url(r'^licence$', 'pgaweb.views.licence', name='licence'),
    url(r'^privacy_policy$', 'pgaweb.views.privacy_policy', name='privacy_policy'),
    url(r'^development$', 'pgaweb.views.development_index', name='development_index'),
    url(r'^development/resources$', 'pgaweb.views.development_resources', name='development_resources'),
    url(r'^development/team$', 'pgaweb.views.development_team', name='development_team'),
    url(r'^support$', 'pgaweb.views.support_index', name='support_index'),
    url(r'^support/issues$', 'pgaweb.views.support_issues', name='support_issues'),
    url(r'^support/list$', 'pgaweb.views.support_list', name='support_list'),

    url(r'^download$', 'download.views.index', name='download_index'),
    url(r'^download/(?P<slug>[\w-]+)$', 'download.views.download_list', name='download_list'),

    url(r'^faq$', 'faq.views.index', name='faq'),

    url(r'^versions.json$', 'versions.views.index', name='versions.json'),

    url(r'^admin/', include(admin.site.urls)),
]
