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

import settings


handler400 = 'pgaweb.views.bad_request'
handler403 = 'pgaweb.views.permission_denied'
handler404 = 'pgaweb.views.page_not_found'
handler500 = 'pgaweb.views.server_error'


urlpatterns = [
    url(r'^$', 'pgaweb.views.index', name='index'),
    url(r'^contributing/$', 'pgaweb.views.contributing', name='contributing'),
    url(r'^docs/$', 'pgaweb.views.docs', name='docs'),
    url(r'^features/$', 'pgaweb.views.features', name='features'),
    url(r'^licence/$', 'pgaweb.views.licence', name='licence'),
    url(r'^privacy_policy/$', 'pgaweb.views.privacy_policy', name='privacy_policy'),
    url(r'^screenshots/$', 'pgaweb.views.screenshots', name='screenshots'),

    url(r'^development/$', 'pgaweb.views.development_index', name='development_index'),
    url(r'^development/resources/$', 'pgaweb.views.development_resources', name='development_resources'),
    url(r'^development/team/$', 'pgaweb.views.development_team', name='development_team'),

    url(r'^support/$', 'pgaweb.views.support_index', name='support_index'),
    url(r'^support/issues/$', 'pgaweb.views.support_issues', name='support_issues'),
    url(r'^support/list/$', 'pgaweb.views.support_list', name='support_list'),

    url(r'^download/', include('download.urls')),

    url(r'^faq/$', 'faq.views.index', name='faq'),

    url(r'^versions.json$', 'versions.views.index', name='versions.json'),

    url(r'^admin/', include(admin.site.urls))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + [
        url(r'^400/$', 'pgaweb.views.bad_request'),
        url(r'^403/$', 'pgaweb.views.permission_denied'),
        url(r'^404/$', 'pgaweb.views.page_not_found'),
        url(r'^500/$', 'pgaweb.views.server_error')
    ]

