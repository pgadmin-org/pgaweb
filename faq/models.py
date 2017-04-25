##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.db import models


class Category(models.Model):
    order = models.IntegerField(null=False, default=0)
    name = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        ordering = ('order',)
        verbose_name_plural = "FAQ Categories"

    def __unicode__(self):
        return self.name


class Faq(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    order = models.IntegerField(null=False, default=0)
    active = models.BooleanField(null=False, blank=False)
    question = models.CharField(null=False, blank=False, max_length=250)
    answer = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('category','order')
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __unicode__(self):
       return self.question