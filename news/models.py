##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from datetime import date

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label != 'admin.LogEntry':
        cache.clear()


class News(models.Model):
    display = models.BooleanField(null=False, blank=False, default=False)
    date = models.DateField(null=False, blank=False, default=date.today)
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    @property
    def display_date(self):
        return self.date.strftime("%Y-%m-%d")

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = "News Articles"

    def __str__(self):
       return '%s - %s' % (self.display_date, self.title)