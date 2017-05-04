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

admin.site.register(Package)
admin.site.register(Distribution)
admin.site.register(Version)
admin.site.register(Download)
