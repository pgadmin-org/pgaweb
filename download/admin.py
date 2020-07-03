##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.contrib import admin

from .models import Package, Distribution, Version, Download


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug', 'active')
    list_filter = ('active', )


class DistributionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_package', 'order', 'slug', 'active')
    list_filter = ('active', 'package__name')

    def get_package(self, obj):
        return obj.package.name

    get_package.admin_order_field = 'package'
    get_package.short_description = 'Package Name'


class VersionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'pre_release', 'released', 'active')
    list_filter = ('active', 'package__name', 'pre_release', 'released')


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active')
    list_filter = ('active', 'version__package__name', 'distribution', 'version')


admin.site.register(Package, PackageAdmin)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Download, DownloadAdmin)
