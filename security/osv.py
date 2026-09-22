##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

# Helpers for fetching pgAdmin 4 vulnerabilities from the OSV.dev database and
# normalising them into a plain dictionary form. pgAdmin 4 is published to PyPI
# as 'pgadmin4', so we can query OSV by package rather than by fuzzy keyword,
# which gives reliable, version-aware results including cross-referenced
# CVE/GHSA identifiers.
#
# This module deliberately depends only on the Python standard library so that
# the OSV-facing logic stays simple and independently testable; the Django
# management command is responsible for persisting the results.

import json
import urllib.error
import urllib.request

OSV_QUERY_URL = 'https://api.osv.dev/v1/query'
OSV_VULN_URL = 'https://api.osv.dev/v1/vulns/{0}'

# A human-friendly link to the advisory on the OSV web UI.
OSV_WEB_URL = 'https://osv.dev/vulnerability/{0}'

# The PyPI package name that pgAdmin 4 is distributed under.
DEFAULT_ECOSYSTEM = 'PyPI'
DEFAULT_PACKAGE = 'pgadmin4'

# Which source's record to keep when more than one describes the same CVE,
# most preferred first. See merge_duplicates() for why the order is this way
# round; anything not listed sorts last but is still kept if it is the only
# record for that CVE.
SOURCE_PREFERENCE = ('GHSA-', 'PYSEC-', 'CVE-')


class OSVError(Exception):
    """Raised when an OSV request cannot be completed."""


def fetch_json(url, payload=None, timeout=30):
    """POST (if payload given) or GET a URL and return the decoded JSON."""
    data = None
    headers = {'Accept': 'application/json'}

    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    request = urllib.request.Request(url, data=data, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise OSVError("OSV request to {0} failed: HTTP {1} {2}"
                       .format(url, e.code, e.reason))
    except urllib.error.URLError as e:
        raise OSVError("OSV request to {0} failed: {1}".format(url, e.reason))


def query_vuln_ids(ecosystem, package):
    """Return the list of vulnerability IDs affecting the given package.

    The /v1/query endpoint returns summary records that may omit some fields
    (notably the full severity list), so we only use it to discover the IDs and
    fetch the full record for each one separately.
    """
    payload = {'package': {'ecosystem': ecosystem, 'name': package}}
    result = fetch_json(OSV_QUERY_URL, payload=payload)

    vulns = result.get('vulns', []) or []
    return [v['id'] for v in vulns if 'id' in v]


def fetch_vuln(vuln_id):
    """Fetch the full OSV record for a single vulnerability ID."""
    return fetch_json(OSV_VULN_URL.format(vuln_id))


def pick_cve_id(record):
    """Prefer a CVE identifier from the record's aliases, falling back to the
    OSV/GHSA id so we always have something to display."""
    for alias in record.get('aliases', []):
        if alias.startswith('CVE-'):
            return alias
    return record.get('id')


def extract_severity(record):
    """Pull a CVSS vector and (where available) a numeric base score out of an
    OSV record.

    OSV stores severity as a list of {type, score} entries where 'score' is the
    CVSS vector string, not a number. We surface the vector verbatim and compute
    the base score from it so the page has something sortable; a qualitative
    label from database_specific is used as a fallback when no vector is
    present.
    """
    # Highest CVSS version first, since CVSS_V4 sorts after CVSS_V3.
    vectors = sorted(
        (entry['score'] for entry in record.get('severity', []) or []
         if entry.get('type', '').startswith('CVSS_V') and entry.get('score')),
        reverse=True)

    # The highest version we can actually score, rather than simply the
    # highest. A record carrying both a 4.0 and a 3.1 vector, which is how
    # every advisory published since mid 2026 arrives, would otherwise show
    # the 4.0 vector and no score at all, because cvss_base_score cannot
    # compute 4.0: its scoring is a lookup table rather than a formula, and
    # this module deliberately has no dependencies to bring one in. Since the
    # score and the vector are displayed together, they have to come from the
    # same vector or the page would be quoting one version's metrics beside
    # another version's number.
    vector = vectors[0] if vectors else None
    base_score = None
    for candidate in vectors:
        score = cvss_base_score(candidate)
        if score is not None:
            vector, base_score = candidate, score
            break

    label = None
    if base_score is not None:
        label = severity_label(base_score)
    else:
        # GHSA-sourced records often carry a qualitative severity here.
        label = (record.get('database_specific', {}) or {}).get('severity')
        if label:
            label = label.title()

    return {'cvss_vector': vector, 'base_score': base_score, 'label': label}


def severity_label(score):
    """Map a CVSS base score to its qualitative band (CVSS v3.x / v4.0)."""
    if score >= 9.0:
        return 'Critical'
    if score >= 7.0:
        return 'High'
    if score >= 4.0:
        return 'Medium'
    if score > 0.0:
        return 'Low'
    return 'None'


def cvss_base_score(vector):
    """Compute a CVSS v3.0/v3.1 base score from its vector string.

    Returns None for vectors we cannot parse (e.g. CVSS v4.0, whose scoring is
    materially different and not worth reimplementing here).
    """
    if not vector or not vector.startswith('CVSS:3'):
        return None

    metrics = {}
    for part in vector.split('/')[1:]:
        if ':' in part:
            key, value = part.split(':', 1)
            metrics[key] = value

    weights = {
        'AV': {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.2},
        'AC': {'L': 0.77, 'H': 0.44},
        'PR': {'N': 0.85, 'L': 0.62, 'H': 0.27},      # adjusted below if scope changes
        'UI': {'N': 0.85, 'R': 0.62},
        'C': {'H': 0.56, 'L': 0.22, 'N': 0.0},
        'I': {'H': 0.56, 'L': 0.22, 'N': 0.0},
        'A': {'H': 0.56, 'L': 0.22, 'N': 0.0},
    }

    try:
        scope_changed = metrics['S'] == 'C'

        # Privileges Required uses different weights when scope is changed.
        pr = metrics['PR']
        if scope_changed:
            pr_weight = {'N': 0.85, 'L': 0.68, 'H': 0.5}[pr]
        else:
            pr_weight = weights['PR'][pr]

        iss = 1 - ((1 - weights['C'][metrics['C']]) *
                   (1 - weights['I'][metrics['I']]) *
                   (1 - weights['A'][metrics['A']]))

        if scope_changed:
            impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
        else:
            impact = 6.42 * iss

        exploitability = (8.22 * weights['AV'][metrics['AV']] *
                          weights['AC'][metrics['AC']] * pr_weight *
                          weights['UI'][metrics['UI']])

        if impact <= 0:
            return 0.0

        if scope_changed:
            base = min(1.08 * (impact + exploitability), 10.0)
        else:
            base = min(impact + exploitability, 10.0)

        # CVSS rounds up to one decimal place.
        return round_up(base)
    except KeyError:
        return None


def round_up(value):
    """CVSS 'roundup': round up to the nearest tenth."""
    integer = int(round(value * 100000))
    if integer % 10000 == 0:
        return integer / 100000.0
    return (int(integer / 10000) + 1) / 10.0


def extract_affected(record, ecosystem, package):
    """Return the introduced/fixed version ranges for our package only."""
    ranges = []
    fixed_versions = []

    for affected in record.get('affected', []) or []:
        pkg = affected.get('package', {})
        if pkg.get('ecosystem') != ecosystem or pkg.get('name') != package:
            continue

        for rng in affected.get('ranges', []) or []:
            introduced = None
            fixed = None
            for event in rng.get('events', []) or []:
                if 'introduced' in event:
                    introduced = event['introduced']
                if 'fixed' in event:
                    fixed = event['fixed']
                    fixed_versions.append(fixed)
            ranges.append({'introduced': introduced, 'fixed': fixed})

    return ranges, sorted(set(fixed_versions))


def normalise(record, ecosystem, package):
    """Reduce a full OSV record to the fields the security page needs."""
    osv_id = record.get('id')
    ranges, fixed_versions = extract_affected(record, ecosystem, package)
    severity = extract_severity(record)

    return {
        'cve_id': pick_cve_id(record),
        'osv_id': osv_id,
        'aliases': record.get('aliases', []),
        'summary': record.get('summary', ''),
        'details': record.get('details', ''),
        'cvss_vector': severity['cvss_vector'],
        'base_score': severity['base_score'],
        'severity': severity['label'],
        'affected_ranges': ranges,
        'fixed_versions': fixed_versions,
        'published': record.get('published'),
        'modified': record.get('modified'),
        'references': [r.get('url') for r in record.get('references', [])
                       if r.get('url')],
        'osv_url': OSV_WEB_URL.format(osv_id) if osv_id else '',
    }


def source_rank(osv_id):
    """How much we would rather keep this record, lower being better.

    Used only to choose between records describing the same CVE. GHSA wins
    because GitHub assigns an advisory one identifier and keeps it, whereas
    the PYSEC identifiers for pgAdmin were all reassigned within a single
    year for CVEs going back to 2022, so keeping those as the stable key
    would mean the whole table churning whenever that happens again.
    """
    for index, prefix in enumerate(SOURCE_PREFERENCE):
        if osv_id.startswith(prefix):
            return index
    return len(SOURCE_PREFERENCE)


def merge_duplicates(advisories):
    """Collapse advisories that describe the same CVE into one.

    OSV returns one record per source, so a single pgAdmin vulnerability
    arrives twice, once from the GitHub Advisory Database and once from the
    PyPA database: at the time of writing every one of the 28 CVEs affecting
    pgAdmin came back as both a GHSA and a PYSEC record, and the security page
    therefore listed each vulnerability twice. The two carry the same summary,
    details and severity, so which one is kept matters less than keeping only
    one of them.

    References are unioned rather than taken from the winner alone, since the
    record we discard usually links to a couple of places the other does not,
    and a reader losing a link to the upstream advisory would be a poor trade
    for tidiness. Aliases are unioned for the same reason: they are how a
    reader searching for the identifier we dropped still finds the advisory.

    Anything without a CVE identifier is passed through untouched, there being
    nothing to match it against.
    """
    merged = {}
    passthrough = []

    for advisory in advisories:
        cve_id = advisory.get('cve_id', '')
        if not cve_id.startswith('CVE-'):
            passthrough.append(advisory)
            continue

        existing = merged.get(cve_id)
        if existing is None:
            merged[cve_id] = advisory
            continue

        keep, drop = existing, advisory
        if source_rank(advisory['osv_id']) < source_rank(existing['osv_id']):
            keep, drop = advisory, existing

        keep['references'] = union(keep['references'], drop['references'])
        keep['aliases'] = union(keep['aliases'], drop['aliases'],
                                [drop['osv_id']])
        merged[cve_id] = keep

    return passthrough + list(merged.values())


def union(*lists):
    """The given lists concatenated, keeping the first of each duplicate.

    Order is preserved rather than sorted, because the first source's
    references are the ones we would have shown before this merging existed.
    """
    seen = set()
    result = []
    for values in lists:
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
    return result


def fetch_advisories(ecosystem=DEFAULT_ECOSYSTEM, package=DEFAULT_PACKAGE):
    """Fetch and normalise every advisory affecting the given package."""
    advisories = []
    for vuln_id in query_vuln_ids(ecosystem, package):
        record = fetch_vuln(vuln_id)
        advisories.append(normalise(record, ecosystem, package))
    return merge_duplicates(advisories)
