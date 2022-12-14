##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.conf.urls import include, url
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
    url(r'^$', pgaweb_views.index, name='index'),
    url(r'^ads.txt$', pgaweb_views.ads_txt, name='ads_txt'),
    url(r'^contributing/$', pgaweb_views.contributing, name='contributing'),
    url(r'^features/$', pgaweb_views.features, name='features'),
    url(r'^licence/$', pgaweb_views.licence, name='licence'),
    url(r'^privacy_policy/$', pgaweb_views.privacy_policy, name='privacy_policy'),
    url(r'^screenshots/$', pgaweb_views.screenshots, name='screenshots'),

    url(r'^development/$', pgaweb_views.development_index, name='development_index'),
    url(r'^development/resources/$', pgaweb_views.development_resources,
        name='development_resources'),
    url(r'^development/team/$', pgaweb_views.development_team, name='development_team'),
    url(r'^development/translations/$', pgaweb_views.development_translations,
        name='development_translations'),
    url(r'^styleguide/$', pgaweb_views.styleguide_redirect, name='styleguide_redirect'),
    url(r'^styleguide/(?P<page>[a-zA-Z]+)(?:/(?P<section>[a-zA-Z_]+))?/$', pgaweb_views.styleguide_index,
        name='styleguide_index'),
    url(r'^support/$', pgaweb_views.support_index, name='support_index'),
    url(r'^support/issues/$', pgaweb_views.support_issues, name='support_issues'),
    url(r'^support/list/$', pgaweb_views.support_list, name='support_list'),

    url(r'^blogs/$', blogs_views.index, name='blogs'),
    url(r'^blog.rss$', blog_feed.LatestEntriesFeed(), name='blog_feed'),

    url(r'^docs/', include('docs.urls')),

    url(r'^download/', include('download.urls')),

    url(r'^faq/$', faq_views.index, name='faq'),

    url(r'^news/$', news_views.index, name='news'),
    url(r'^news.rss$', news_feed.LatestEntriesFeed(), name='news_feed'),

    url(r'^search/', include('search.urls')),

    url(r'^versions.json$', versions_views.index, name='versions.json'),

    url(r'^videos/$', videos_views.index, name='videos'),
    url(r'^videos.rss$', video_feed.LatestEntriesFeed(), name='video_feed'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + [
        url(r'^400/$', pgaweb_views.bad_request),
        url(r'^403/$', pgaweb_views.permission_denied),
        url(r'^404/$', pgaweb_views.page_not_found),
        url(r'^500/$', pgaweb_views.server_error)
    ]
