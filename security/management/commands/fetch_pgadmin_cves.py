##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

# Fetch the list of known pgAdmin 4 vulnerabilities from the OSV.dev database
# and upsert them into the SecurityAdvisory table, so the security page can be
# served straight from the database with no live dependency on OSV.
#
# Intended to be run periodically (e.g. from cron):
#
#     ./manage.py fetch_pgadmin_cves
#
# The whole refresh runs in a single transaction, so a failure part way through
# leaves the existing data untouched rather than half-updated. Editor-owned
# fields ('notes' and 'suppressed') are never written by this command, so any
# curation survives a refresh.

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from security import osv
from security.models import SecurityAdvisory


class Command(BaseCommand):
    help = ('Fetch pgAdmin 4 vulnerabilities from OSV.dev and update the '
            'security advisories table.')

    def add_arguments(self, parser):
        parser.add_argument('--ecosystem', default=osv.DEFAULT_ECOSYSTEM,
                            help='OSV ecosystem (default: %(default)s)')
        parser.add_argument('--package', default=osv.DEFAULT_PACKAGE,
                            help='package name (default: %(default)s)')
        parser.add_argument('--prune', action='store_true',
                            help='delete advisories OSV no longer reports')

    def handle(self, *args, **options):
        try:
            advisories = osv.fetch_advisories(options['ecosystem'],
                                              options['package'])
        except osv.OSVError as e:
            raise CommandError(str(e))

        now = timezone.now()
        seen_ids = []

        with transaction.atomic():
            for advisory in advisories:
                seen_ids.append(advisory['osv_id'])

                # 'defaults' are the OSV-sourced fields; 'notes' and
                # 'suppressed' are intentionally absent so existing values are
                # preserved across refreshes.
                SecurityAdvisory.objects.update_or_create(
                    osv_id=advisory['osv_id'],
                    defaults={
                        'cve_id': advisory['cve_id'],
                        'summary': advisory['summary'],
                        'details': advisory['details'],
                        'cvss_vector': advisory['cvss_vector'] or '',
                        'base_score': advisory['base_score'],
                        'severity': advisory['severity'] or '',
                        'affected_ranges': advisory['affected_ranges'],
                        'fixed_versions': advisory['fixed_versions'],
                        'references': advisory['references'],
                        'published': parse_datetime(advisory['published'])
                        if advisory['published'] else None,
                        'modified': parse_datetime(advisory['modified'])
                        if advisory['modified'] else None,
                        'osv_url': advisory['osv_url'],
                        'last_seen': now,
                    },
                )

            stale = SecurityAdvisory.objects.exclude(osv_id__in=seen_ids)
            stale_count = stale.count()
            if options['prune']:
                stale.delete()

        self.stdout.write(self.style.SUCCESS(
            "Imported {0} advisories from OSV.".format(len(seen_ids))))
        if stale_count:
            if options['prune']:
                self.stdout.write(
                    "Pruned {0} advisory(ies) no longer reported by OSV."
                    .format(stale_count))
            else:
                self.stdout.write(self.style.WARNING(
                    "{0} advisory(ies) in the database are no longer reported "
                    "by OSV; re-run with --prune to remove them."
                    .format(stale_count)))
