##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.contrib import admin

from .models import Version


class VersionAdmin(admin.ModelAdmin):
    list_display = ('package', 'version_str', 'version_int', 'download_url', 'active', 'auto_update_url')
    list_filter = ('active', 'version_str')


admin.site.register(Version, VersionAdmin)
