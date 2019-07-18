##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label != 'admin.LogEntry':
        cache.clear()


class Version(models.Model):
    active = models.BooleanField(null=False, blank=False)
    package = models.CharField(null=False, blank=False, max_length=50)
    version_str = models.CharField(null=False, blank=False, max_length=20, verbose_name="Version (String)")
    version_int = models.IntegerField(null=False, blank=False, verbose_name="Version (Integer)")
    download_url = models.CharField(null=False, blank=False, max_length=150, verbose_name="Download URL")

    class Meta:
        ordering = ('version_int',)
        unique_together = ('active', 'package',)

    def __str__(self):
       return '%s - v%s' % (self.package, self.version_str)