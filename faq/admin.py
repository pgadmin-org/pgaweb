##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.contrib import admin

from .models import Category, Faq

admin.site.register(Category)
admin.site.register(Faq)
