##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.db import models


class Search(models.Model):
    logged = models.DateTimeField(auto_now_add=True)
    terms = models.TextField(null=False, blank=True)

    class Meta:
        verbose_name_plural = "Searches"
