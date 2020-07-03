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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'question', 'order', 'active')
    list_filter = ('active', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Faq, FaqAdmin)
