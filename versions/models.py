##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from datetime import date
from django.db import models


class Version(models.Model):
    active = models.BooleanField(null=False, blank=False)
    package = models.CharField(null=False, blank=False, max_length=50)
    version_str = models.CharField(null=False, blank=False, max_length=20)
    version_int = models.IntegerField(null=False, blank=False)
    download_url = models.CharField(null=False, blank=False, max_length=150)

    class Meta:
        ordering = ('version_int',)
        unique_together = ('active', 'package',)

    def __unicode__(self):
       return '%s - v%s' % (self.package, self.version_str)