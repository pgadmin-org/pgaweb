##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.conf.urls import handler400, handler403, handler404, handler500, include, url
from django.contrib import admin
from pgaweb import views as pgaweb_views
from faq import views as faq_views
from search import views as search_views
from versions import views as versions_views

from . import settings


handler400 = 'pgaweb.views.bad_request'
handler403 = 'pgaweb.views.permission_denied'
handler404 = 'pgaweb.views.page_not_found'
handler500 = 'pgaweb.views.server_error'


urlpatterns = [
    url(r'^$', pgaweb_views.index, name='index'),
    url(r'^ads.txt$', pgaweb_views.ads_txt, name='ads_txt'),
    url(r'^contributing/$', pgaweb_views.contributing, name='contributing'),
    url(r'^features/$', pgaweb_views.features, name='features'),
    url(r'^licence/$', pgaweb_views.licence, name='licence'),
    url(r'^privacy_policy/$', pgaweb_views.privacy_policy, name='privacy_policy'),
    url(r'^screenshots/$', pgaweb_views.screenshots, name='screenshots'),
    url(r'^try/$', pgaweb_views.try_pgadmin, name='try_pgadmin'),

    url(r'^development/$', pgaweb_views.development_index, name='development_index'),
    url(r'^development/resources/$', pgaweb_views.development_resources, name='development_resources'),
    url(r'^development/team/$', pgaweb_views.development_team, name='development_team'),

    url(r'^styleguide/$', pgaweb_views.styleguide_index, name='styleguide_index'),

    url(r'^support/$', pgaweb_views.support_index, name='support_index'),
    url(r'^support/issues/$', pgaweb_views.support_issues, name='support_issues'),
    url(r'^support/list/$', pgaweb_views.support_list, name='support_list'),

    url(r'^docs/', include('docs.urls')),

    url(r'^download/', include('download.urls')),

    url(r'^faq/$', faq_views.index, name='faq'),

    url(r'^search/', include('search.urls')),

    url(r'^versions.json$', versions_views.index, name='versions.json'),

    url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns = urlpatterns + [
        url(r'^400/$', pgaweb_views.bad_request),
        url(r'^403/$', pgaweb_views.permission_denied),
        url(r'^404/$', pgaweb_views.page_not_found),
        url(r'^500/$', pgaweb_views.server_error)
    ]
