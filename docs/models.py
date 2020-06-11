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
from django.urls import reverse
from download.models import Version
import tsvector_field


@receiver(post_save)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label != 'admin.LogEntry':
        cache.clear()


class Page(models.Model):
    """
    Stores documentation pages that are not external files. Related to
    :model:`docs.Document`,
    """
    version = models.ForeignKey(Version, on_delete=models.CASCADE,
                                help_text="Select the Product Version to "
                                          "which this page applies.")
    file = models.CharField(null=False, blank=False, max_length=100,
                            help_text="The file name of the page")
    title = models.CharField(null=False, blank=False, max_length=500,
                             help_text="The title of the page")
    header = models.TextField(null=False, blank=True,
                              help_text="The header block for the page.")
    contents = models.TextField(null=False, blank=True,
                                help_text="The contents block of the page.")
    body = models.TextField(null=False, blank=True,
                            help_text="The body of the page.")
    search = tsvector_field.SearchVectorField([
        tsvector_field.WeightedColumn('title', 'A'),
        tsvector_field.WeightedColumn('body', 'D'),
    ], 'english', blank=True)

    @property
    def url(self):
        return reverse('page', args=[self.version.package.slug,
                                     self.version.name,
                                     self.file])

    class Meta:
        unique_together = ['version', 'file']
        ordering = ('version', 'title')

    def __str__(self):
        return self.title
