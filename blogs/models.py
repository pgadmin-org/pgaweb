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
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from utils import varnish_ban


@receiver(post_save)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label == 'blogs.Blog':
        # The homepage, everything under /blogs, and the blog feed
        varnish_ban('^' + reverse('index') + '$')
        varnish_ban('^' + reverse('blogs') + '$')
        varnish_ban('^' + reverse('blog_feed') + '$')


class Blog(models.Model):
    display = models.BooleanField(null=False, blank=False, default=False,
                                  help_text='Display the blog on the home '
                                            'page.')
    disable = models.BooleanField(null=False, blank=False, default=False,
                                  help_text='Hide the blog from all pages.')
    date = models.DateField(null=False, blank=False, default=date.today)
    title = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=200, null=False, blank=False)
    summary = models.TextField(null=False, blank=False)
    url = models.CharField(max_length=250, null=False, blank=False,
                           help_text='The URL of the blog')

    @property
    def display_date(self):
        return self.date.strftime("%Y-%m-%d")

    class Meta:
        ordering = ('-date', '-id')

    def __str__(self):
        return '%s - %s' % (self.display_date, self.title)
