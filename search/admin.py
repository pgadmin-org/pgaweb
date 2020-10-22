##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.contrib import admin

from .models import Search


class SearchAdmin(admin.ModelAdmin):
    list_display = ('logged', 'terms')
    readonly_fields = ('logged', 'terms')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Search, SearchAdmin)
