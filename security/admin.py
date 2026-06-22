##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.contrib import admin

from .models import SecurityAdvisory


class SecurityAdvisoryAdmin(admin.ModelAdmin):
    list_display = ('cve_id', 'osv_id', 'severity', 'base_score',
                    'fixed_versions', 'suppressed', 'published')
    list_filter = ('severity', 'suppressed')
    search_fields = ('cve_id', 'osv_id', 'summary')
    ordering = ('-base_score', '-published')

    # Everything sourced from OSV is read-only; editors only own 'notes' and
    # 'suppressed', which the importer never overwrites.
    readonly_fields = ('osv_id', 'cve_id', 'summary', 'details', 'cvss_vector',
                       'base_score', 'severity', 'affected_ranges',
                       'fixed_versions', 'references', 'published', 'modified',
                       'osv_url', 'last_seen')

    def has_add_permission(self, request):
        # Advisories are created by the importer, not by hand.
        return False


admin.site.register(SecurityAdvisory, SecurityAdvisoryAdmin)
