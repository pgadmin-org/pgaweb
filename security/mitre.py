##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

# Helpers for reading CVE records from MITRE's CVE Services API, used to fill
# in what OSV lacks for a pgAdmin advisory.
#
# Since mid 2026 most pgAdmin CVEs have reached OSV only as records converted
# from the CVE list, with affected ranges expressed as git commits rather than
# release versions, and often with a CVSS 4.0 vector alone, which this site
# cannot score (see osv.cvss_base_score). The CVE record itself, as published
# by the PostgreSQL project as the CNA, gives the affected versions as release
# numbers and carries a CVSS 3.1 vector alongside the 4.0 one, so it has both
# of the things the security page would otherwise show nothing for.
#
# MITRE's API looks records up by identifier only and cannot search by
# product, which is why OSV remains the source of the list of advisories.
#
# Like osv.py, this depends only on the standard library.

from security import osv

CVE_RECORD_URL = 'https://cveawg.mitre.org/api/cve/{0}'

# The product name the PostgreSQL CNA uses for pgAdmin 4 in its records.
PRODUCT = 'pgAdmin 4'

# CVE record metric keys, most preferred first, mapped to the OSV severity
# type each corresponds to.
CVSS_METRICS = (('cvssV4_0', 'CVSS_V4'), ('cvssV3_1', 'CVSS_V3'),
                ('cvssV3_0', 'CVSS_V3'))


def fetch_record(cve_id):
    """Fetch the CVE record for a single CVE identifier."""
    return osv.fetch_json(CVE_RECORD_URL.format(cve_id))


def containers(record):
    """The CNA container followed by any ADP containers, which is the order
    in which their data should be trusted: the CNA is the project that
    assigned the CVE, whilst an ADP (such as CISA) adds to it afterwards."""
    found = record.get('containers', {}) or {}
    return [found.get('cna', {}) or {}] + list(found.get('adp', []) or [])


def extract_ranges(record):
    """Return the introduced/fixed version ranges for pgAdmin 4, in the form
    osv.extract_affected returns them.

    Only 'affected' entries with a 'lessThan' bound give us a version that
    fixes the issue. A 'lessThanOrEqual' bound names the last vulnerable
    release rather than the first fixed one, and free-text versions such as
    'versions prior to v6.14' cannot be relied upon, so both are ignored
    rather than guessed at.
    """
    ranges = []
    fixed_versions = []

    cna = containers(record)[0]
    for affected in cna.get('affected', []) or []:
        if affected.get('product') != PRODUCT:
            continue

        for version in affected.get('versions', []) or []:
            fixed = version.get('lessThan')
            if version.get('status') != 'affected' or not fixed \
                    or fixed == '*':
                continue

            introduced = version.get('version')
            if introduced == '0':
                introduced = None

            ranges.append({'introduced': introduced, 'fixed': fixed})
            fixed_versions.append(fixed)

    return ranges, sorted(set(fixed_versions))


def extract_severity(record):
    """Return the CVSS vectors in the record as OSV-style severity entries, so
    that osv.extract_severity can choose between them by its usual rules."""
    severity = []
    for container in containers(record):
        for metric in container.get('metrics', []) or []:
            for key, osv_type in CVSS_METRICS:
                vector = (metric.get(key) or {}).get('vectorString')
                if vector:
                    severity.append({'type': osv_type, 'score': vector})
    return severity


def fill_gaps(advisory, record):
    """Fill the version and severity fields that OSV left empty from the CVE
    record. Anything OSV did provide is left alone, so the advisories OSV
    already describes fully are unchanged by this."""
    if not advisory['fixed_versions']:
        ranges, fixed_versions = extract_ranges(record)
        if fixed_versions:
            advisory['affected_ranges'] = ranges
            advisory['fixed_versions'] = fixed_versions

    if advisory['base_score'] is None:
        severity = osv.extract_severity({'severity': extract_severity(record)})
        if severity['base_score'] is not None:
            advisory['cvss_vector'] = severity['cvss_vector']
            advisory['base_score'] = severity['base_score']
            advisory['severity'] = severity['label']

    return advisory


def needs_filling(advisory):
    """Whether an advisory has gaps a CVE record might fill."""
    return advisory['cve_id'].startswith('CVE-') and (
        not advisory['fixed_versions'] or advisory['base_score'] is None)


def complete_advisories(advisories):
    """Fill in each advisory's gaps from its CVE record, fetching records
    only for the advisories that have gaps to fill."""
    for advisory in advisories:
        if needs_filling(advisory):
            fill_gaps(advisory, fetch_record(advisory['cve_id']))
    return advisories
