##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import datetime
import re

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


@receiver(post_save)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label != 'admin.LogEntry':
        cache.clear()


def version_slugify(value):
    """
    Basically the same as django.template.defaultfilters.slugify, except
    that we don't support Unicode (don't need to), and we leave full
    stops alone.
    """
    value = str(value)
    value = re.sub(r'[^\.\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


class Package(models.Model):
    order = models.IntegerField(null=False, default=0)
    name = models.CharField(null=False, blank=False, max_length=50)
    active = models.BooleanField(null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    slug = models.SlugField(null=False, blank=True, max_length=100, unique=True,
                            help_text="The string to use to identify this "
                                      "item in URLs. Leave blank to "
                                      "auto-generate.")

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Package, self).save(*args, **kwargs)


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

    def __str__(self):
        return "%s (%s)" % (self.package, self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify("%s %s" % (self.package, self.name))

        super(Distribution, self).save(*args, **kwargs)


class Version(models.Model):
    package = models.ForeignKey('Package', on_delete=models.PROTECT)
    name = models.CharField(null=False, blank=False, max_length=50)
    # Note that this slug field is defined as a CharField as we allow a custom
    # format (specifically, we allow full stops to remain.
    slug = models.CharField(null=False, blank=True, max_length=50)
    active = models.BooleanField(null=False, blank=False)
    released = models.DateField(null=True, blank=True, default=datetime.date.today)
    pre_release = models.BooleanField(null=False, blank=False, default=False)
    pdf_doc = models.BooleanField(null=False, blank=False, default=False)
    epub_doc = models.BooleanField(null=False, blank=False, default=False)
    tarball_doc = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = ('package__order', 'pre_release', '-released', 'name')

    def list_string(self):
        if self.name[0].isdigit():
            return "Version %s" % self.name
        else:
            return "%s" % self.name

    def __str__(self):
        if self.name[0].isdigit():
            return "%s v%s" % (self.package, self.name)
        else:
            return "%s %s" % (self.package, self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = version_slugify("%s %s" % (self.package, self.name))

        super(Version, self).save(*args, **kwargs)


class Download(models.Model):
    distribution = models.ForeignKey('Distribution', on_delete=models.PROTECT)
    version = models.ForeignKey('Version', on_delete=models.PROTECT)
    active = models.BooleanField(null=False, blank=False)
    download_url = models.CharField(null=False, blank=False, max_length=250)
    notes_url = models.CharField(null=False, blank=True, max_length=250)

    class Meta:
        ordering = ('version', 'distribution')

    def __str__(self):
        return "%s (%s)" % (self.version, self.distribution.name)
