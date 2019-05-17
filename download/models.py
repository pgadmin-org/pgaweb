##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import datetime

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


@receiver(post_save)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label != 'admin.LogEntry':
        print("Clearing the Django cache...")
        cache.clear()


class Package(models.Model):
    order = models.IntegerField(null=False, default=0)
    name = models.CharField(null=False, blank=False, max_length=50)
    active = models.BooleanField(null=False, blank=False)
    description = models.TextField(null=False, blank=True)

    class Meta:
        ordering = ('order', 'name')

    def __unicode__(self):
        return self.name


class Distribution(models.Model):
    package = models.ForeignKey('Package', on_delete=models.PROTECT)
    order = models.IntegerField(null=False, default=0)
    name = models.CharField(null=False, blank=False, max_length=50)
    slug = models.SlugField(null=False, blank=True)
    active = models.BooleanField(null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    notes = models.TextField(null=False, blank=True)
    maintainer = models.CharField(null=False, blank=False, max_length=100)
    icon = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        ordering = ('order', 'package', 'name')

    def __unicode__(self):
        return "%s (%s)" % (self.package, self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify("%s %s" % (self.package, self.name))

        super(Distribution, self).save(*args, **kwargs)


class Version(models.Model):
    package = models.ForeignKey('Package', on_delete=models.PROTECT)
    name = models.CharField(null=False, blank=False, max_length=50)
    active = models.BooleanField(null=False, blank=False)
    released = models.DateField(null=False, blank=False, default=datetime.date.today)

    class Meta:
        ordering = ('-released', 'name')

    def __unicode__(self):
        return "%s v%s" % (self.package, self.name)


class Download(models.Model):
    distribution = models.ForeignKey('Distribution', on_delete=models.PROTECT)
    version = models.ForeignKey('Version', on_delete=models.PROTECT)
    active = models.BooleanField(null=False, blank=False)
    download_url = models.CharField(null=False, blank=False, max_length=250)
    notes_url = models.CharField(null=False, blank=True, max_length=250)

    class Meta:
        ordering = ('version', 'distribution')

    def __unicode__(self):
        return "%s (%s)" % (self.version, self.distribution.name)
