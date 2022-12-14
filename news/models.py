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
    if kwargs['sender']._meta.label == 'news.News':
        # The index page and news archive/feed
        varnish_ban('^' + reverse('index') + '$')
        varnish_ban('^' + reverse('news') + '$')
        varnish_ban('^' + reverse('news_feed') + '$')


class News(models.Model):
    display = models.BooleanField(null=False, blank=False, default=False,
                                  help_text='Display the article on the home '
                                            'page.')
    disable = models.BooleanField(null=False, blank=False, default=False,
                                  help_text='Hide the article from all pages.')
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
