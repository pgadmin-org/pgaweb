##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.urls import include, re_path
from django.contrib import admin
from pgaweb import views as pgaweb_views
from blogs import views as blogs_views
from blogs import feeds as blog_feed
from faq import views as faq_views
from news import views as news_views
from news import feeds as news_feed
from versions import views as versions_views
from videos import views as videos_views
from videos import feeds as video_feed

from . import settings


handler400 = 'pgaweb.views.bad_request'
handler403 = 'pgaweb.views.permission_denied'
handler404 = 'pgaweb.views.page_not_found'
handler500 = 'pgaweb.views.server_error'


urlpatterns = [
    re_path(r'^$', pgaweb_views.index, name='index'),
    re_path(r'^ads.txt$', pgaweb_views.ads_txt, name='ads_txt'),
    re_path(r'^contributing/$', pgaweb_views.contributing, name='contributing'),
    re_path(r'^features/$', pgaweb_views.features, name='features'),
    re_path(r'^licence/$', pgaweb_views.licence, name='licence'),
    re_path(r'^privacy_policy/$', pgaweb_views.privacy_policy, name='privacy_policy'),
    re_path(r'^screenshots/$', pgaweb_views.screenshots, name='screenshots'),

    re_path(r'^development/$', pgaweb_views.development_index, name='development_index'),
    re_path(r'^development/resources/$', pgaweb_views.development_resources,
        name='development_resources'),
    re_path(r'^development/team/$', pgaweb_views.development_team, name='development_team'),
    re_path(r'^development/translations/$', pgaweb_views.development_translations,
        name='development_translations'),
    re_path(r'^styleguide/$', pgaweb_views.styleguide_redirect, name='styleguide_redirect'),
    re_path(r'^styleguide/(?P<page>[a-zA-Z]+)(?:/(?P<section>[a-zA-Z_]+))?/$', pgaweb_views.styleguide_index,
        name='styleguide_index'),
    re_path(r'^support/$', pgaweb_views.support_index, name='support_index'),
    re_path(r'^support/issues/$', pgaweb_views.support_issues, name='support_issues'),
    re_path(r'^support/list/$', pgaweb_views.support_list, name='support_list'),

    re_path(r'^blogs/$', blogs_views.index, name='blogs'),
    re_path(r'^blog.rss$', blog_feed.LatestEntriesFeed(), name='blog_feed'),

    re_path(r'^docs/', include('docs.urls')),

    re_path(r'^download/', include('download.urls')),

    re_path(r'^faq/$', faq_views.index, name='faq'),

    re_path(r'^news/$', news_views.index, name='news'),
    re_path(r'^news.rss$', news_feed.LatestEntriesFeed(), name='news_feed'),

    re_path(r'^search/', include('search.urls')),

    re_path(r'^versions.json$', versions_views.index, name='versions.json'),

    re_path(r'^videos/$', videos_views.index, name='videos'),
    re_path(r'^videos.rss$', video_feed.LatestEntriesFeed(), name='video_feed'),

    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + [
        re_path(r'^400/$', pgaweb_views.bad_request),
        re_path(r'^403/$', pgaweb_views.permission_denied),
        re_path(r'^404/$', pgaweb_views.page_not_found),
        re_path(r'^500/$', pgaweb_views.server_error)
    ]
