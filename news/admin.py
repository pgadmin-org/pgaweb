##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'display', 'disable')
    list_filter = ('display', 'disable', 'date')
    actions = ['display_on_home', 'hide_from_home', 'enable', 'disable']

    def display_on_home(self, request, queryset):
        queryset.update(display=True)
        msg = "Items have been made visible on the home page"
        self.message_user(request, "%s" % msg)

    display_on_home.short_description = "Display selected items on the home " \
                                        "page"

    def hide_from_home(self, request, queryset):
        queryset.update(display=False)
        msg = "Items have been hidden from the home page"
        self.message_user(request, "%s" % msg)

    hide_from_home.short_description = "Hide selected items on the home page"

    def disable(self, request, queryset):
        queryset.update(disable=True)
        msg = "Items have been disabled from all pages"
        self.message_user(request, "%s" % msg)

    disable.short_description = "Disable the selected items from all pages"

    def enable(self, request, queryset):
        queryset.update(disable=False)
        msg = "Items have been enabled for all pages"
        self.message_user(request, "%s" % msg)

    enable.short_description = "Enable selected items for all pages"


admin.site.register(News, NewsAdmin)
