##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse

from utils import varnish_ban


@receiver(post_save)
@receiver(post_delete)
def clear_the_cache(**kwargs):
    if kwargs['sender']._meta.label == 'security.SecurityAdvisory':
        # The security page
        varnish_ban('^' + reverse('security') + '$')


class SecurityAdvisory(models.Model):
    # Identity. The OSV id is the stable key we upsert on; the CVE id is what we
    # prefer to display, falling back to the OSV/GHSA id when no CVE is assigned.
    osv_id = models.CharField(null=False, blank=False, max_length=64,
                              unique=True)
    cve_id = models.CharField(null=False, blank=True, max_length=32)

    # Description, sourced from OSV.
    summary = models.CharField(null=False, blank=True, max_length=512)
    details = models.TextField(null=False, blank=True)

    # Severity. The vector and base score are derived from OSV; severity is the
    # qualitative band (Critical/High/Medium/Low).
    cvss_vector = models.CharField(null=False, blank=True, max_length=128)
    base_score = models.FloatField(null=True, blank=True)
    severity = models.CharField(null=False, blank=True, max_length=16)

    # Version information, stored as JSON: affected_ranges is a list of
    # {introduced, fixed} dicts and fixed_versions is a flat list of versions.
    affected_ranges = models.JSONField(null=False, blank=True, default=list)
    fixed_versions = models.JSONField(null=False, blank=True, default=list)
    references = models.JSONField(null=False, blank=True, default=list)

    published = models.DateTimeField(null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)
    osv_url = models.URLField(null=False, blank=True)

    # Curation fields. These are owned by the editors, never by the importer, so
    # they survive a refresh: 'notes' is shown on the page only when populated,
    # and 'suppressed' hides an advisory (e.g. a false positive for how pgAdmin
    # is actually shipped) without deleting it.
    notes = models.TextField(null=False, blank=True)
    suppressed = models.BooleanField(null=False, default=False)

    # Set on every refresh so we can tell when the data was last confirmed and
    # prune advisories that OSV no longer reports.
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-base_score', '-published')
        verbose_name = "Security Advisory"
        verbose_name_plural = "Security Advisories"

    def __str__(self):
        return self.cve_id or self.osv_id
