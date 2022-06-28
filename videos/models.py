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
    if kwargs['sender']._meta.label == 'videos.Video':
        # The homepage, everything under /videos, and the video feed
        varnish_ban('^' + reverse('index') + '$')
        varnish_ban('^' + reverse('videos') + '$')
        varnish_ban('^' + reverse('video_feed') + '$')


class Video(models.Model):
    display = models.BooleanField(null=False, blank=False, default=False,
                                  help_text='Display the video on the home '
                                            'page.')
    disable = models.BooleanField(null=False, blank=False, default=False,
                                  help_text='Hide the video from all pages.')
    date = models.DateField(null=False, blank=False, default=date.today)
    title = models.CharField(max_length=200, null=False, blank=False)
    publisher = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    youtube_id = models.CharField(max_length=30, null=False, blank=False,
                                  help_text='The YouTube ID of the video, e.g:'
                                            'uQhTuRlWMxw for the video at '
                                            'https://www.youtube.com/watch?v=uQhTuRlWMxw')

    @property
    def display_date(self):
        return self.date.strftime("%Y-%m-%d")

    class Meta:
        ordering = ('-date', '-id')

    def __str__(self):
        return '%s - %s' % (self.display_date, self.title)
