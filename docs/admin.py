##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import unicode_literals

from django.contrib import admin

from .models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('_get_title',)

    def _get_title(self, obj):
        return str(obj)
    _get_title.allow_tags = True


admin.site.register(Page, PageAdmin)
