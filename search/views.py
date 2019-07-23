##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################


from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from docs.models import Page
from download.models import Version


def search(request):
    """
    Display the search results page.

    :param request: The request object.
    :return: The rendered index page.

    **Template:**

    :template:`search/index.html`
    """
    q = ''

    if request.method == 'GET':

        # Query string
        if 'q' in request.GET and request.GET['q'] != '':
            q = request.GET['q']

        # Version ID
        try:
            v = int(request.GET['v'])
        except Exception as e:
            v = -1

        # Page
        try:
            pg = int(request.GET['pg'])
        except Exception as e:
            pg = 1

    if q != '':
        sql = """SELECT
  ts_rank(search, plainto_tsquery(%s)) AS rank,
  ts_headline(body,
               plainto_tsquery(%s),
               'StartSel=<mark>,StopSel=</mark>,MaxFragments=2,' ||
               'FragmentDelimiter=...,MaxWords=30,MinWords=1') AS headline,
  docs_page.file,
  docs_page.title,
  download_version.name,
  download_version.slug,
  download_package.slug
FROM docs_page
    INNER JOIN download_version ON
        docs_page.version_id = download_version.id
    INNER JOIN download_package ON
        download_version.package_id = download_package.id
WHERE
     search @@ plainto_tsquery(%s) AND
     download_version.active = TRUE"""

        if v != -1:
            sql = sql + ' AND\n     download_version.id = %s'
        else:
            sql = sql + """ AND download_version.id IN (WITH versions AS (
  SELECT
    id,
    row_number() OVER (PARTITION BY package_id ORDER BY released DESC) AS row_number
  FROM download_version WHERE pre_release = False AND released IS NOT NULL
)
SELECT versions.id
FROM versions
WHERE row_number = 1)"""

        # Build the parameter list
        params = [q, q, q]

        if v != -1:
            params.append(v)

        # Add the limit and offset.
        # We get one more result than we need, so the template can decide
        # whether or not there are more results to display.
        sql = sql + '\nORDER BY rank DESC, download_version.name DESC\nLIMIT 25'
        sql = sql + '\nOFFSET ' + str((pg - 1) * 25)

        # Run the query
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

            # Convert the data to a usable format
            results = []
            for row in cursor:
                results.append({'rank': row[0],
                                'headline': row[1],
                                'file': row[2],
                                'title': row[3],
                                'version': row[4],
                                'version_slug': row[5],
                                'package': row[6]})

            # Get the bounds
            # 25 results per previous page, pus the first on this page
            first = (pg - 1) * 25 + 1

            # 25 results per previous page, plus the rows on this page
            last = (pg - 1) * 25 + len(results)

            if len(results) == 0:
                data = {'message': 'No results found for <b>%s</b>' % q}
                data.update({'query': q})
            else:
                data = {'message': 'Search results for <b>%s</b>:' % q}
                data.update({'results': results,
                             'query': q,
                             'page': int(pg),
                             'first': int(first),
                             'last': int(last)})

            return render(request, 'search/index.html', data)

    # Index page
    data = {'message': 'Enter a query and press the search button:'}

    return render(request, 'search/index.html', data)


def versions(request):
    """
    Get a JSON list of product versions

    :param request: The request object.
    :return: A JSON document containing the version numbers
    """
    # Get a list of all active versions
    versions = Version.objects.filter(active=True)

    result = []
    for v in versions:
        result.append((v.id, v.name))

    return JsonResponse(result, safe=False)
