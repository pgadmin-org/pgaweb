#!/usr/bin/env python3

# Connect to the pgaweb database and create a new release
# using the standard options.

import argparse
import psycopg2
import sys


def get_package_id(cursor):
    sql = "SELECT id FROM download_package WHERE name = 'pgAdmin 4';"

    if args.d:
        print("Executing:\n----\n{0}\n----").format(sql)

    try:
        cursor.execute(sql)
    except psycopg2.ProgrammingError as e:
        print("Failed to get the package ID:\n{0}").format(e)
        sys.exit(1)

    try:
        package_id = cursor.fetchone()[0]
    except:
        print("Failed to get the package ID:\nZero rows matched the query.")
        sys.exit(1)

    if args.d:
        print("Package ID: {0}").format(package_id)

    return package_id


def create_version(cursor, package_id, version_name):
    # Note: The Django app will automatically prepend a 'v'
    #       to the version name, so if it's there already,
    #       remove it.
    if version_name.startswith('v'):
        version_name = version_name[1:]

    sql = """WITH e AS (
                 INSERT INTO download_version 
                     (package_id, name, slug, active, released, pre_release, pdf_doc, epub_doc, tarball_doc) 
                 VALUES
                     (%s, %s, %s, false, now()::date, false, true, true, true)
                 ON CONFLICT (package_id, name) DO NOTHING
                 RETURNING id
             )
             SELECT * FROM e
             UNION
                 SELECT id FROM download_version WHERE name = %s;"""

    if args.d:
        print("Executing:\n----\n{0}\nArgs: {1}, '{2}', '{3}', '{4}'\n----") \
              .format(sql, package_id, version_name, version_name, version_name)

    try:
        cursor.execute(sql, (package_id, version_name, version_name, version_name))
    except psycopg2.ProgrammingError as e:
        print("Failed to create the new download version:\n{0}").format(e)
        sys.exit(1)

    try:
        version_id = cursor.fetchone()[0]
    except:
        print("Failed to get the version ID:\nZero rows matched the query.")
        sys.exit(1)

    if args.d:
        print("Version ID: {0}").format(version_id)

    return version_id


def get_distribution_id(cursor, distribution_name, package_id):
    sql = """SELECT id FROM download_distribution 
                 WHERE
                     name = %s AND
                     package_id = %s;"""

    if args.d:
        print("Executing:\n----\n{0}\nArgs: '{1}', {2}\n----") \
              .format(sql, distribution_name, package_id)

    try:
        cursor.execute(sql, (distribution_name, package_id))
    except psycopg2.ProgrammingError as e:
        print("Failed to get the distribution ID:\n{0}").format(e)
        sys.exit(1)

    try:
        distribution_id = cursor.fetchone()[0]
    except:
        print("Failed to get the distribution ID:\nZero rows matched the query.")
        sys.exit(1)

    if args.d:
        print("Distribution ID: {0}").format(distribution_id)

    return distribution_id


def create_download(cursor, distribution_name, version_name, download_url, notes_url):
    sql = """INSERT INTO download_download
                 (distribution_id, version_id, active, download_url, notes_url)
             VALUES
                 (%s, %s, true, %s, %s)
             ON CONFLICT (distribution_id, version_id) DO NOTHING;"""

    distribution_id = get_distribution_id(cursor, distribution_name, package_id)

    if args.d:
        print("Executing:\n----\n{0}\nArgs: {1}, {2}, '{3}', '{4}'\n----") \
              .format(sql, distribution_id, version_id,
                      download_url.format(version_name),
                      notes_url.format(version_name[1:].replace('.', '_')))

    try:
        cursor.execute(sql, (distribution_id, version_id,
                             download_url.format(version_name),
                             notes_url.format(version_name[1:].replace('.', '_'))))
    except psycopg2.ProgrammingError as e:
        print("Failed to create the new download:\n{0}").format(e)
        sys.exit(1)


# Command line arguments
parser = argparse.ArgumentParser(description='Create a new pgAdmin release.')
parser.add_argument('version', metavar='<pgAdmin version>', nargs=1,
                   help='the pgAdmin version number to be released')
parser.add_argument('-d', action='store_true',
                   help='display debug output')

args = parser.parse_args()

# Connect to the database
try:
    conn = psycopg2.connect("dbname='pgaweb'")
except psycopg2.OperationalError as e:
    print("Unable to connect to the database:\n{0}").format(e)
    sys.exit(1)

cursor = conn.cursor()

# Get the package ID
package_id = get_package_id(cursor)

# Create the version
version_id = create_version(cursor, package_id, args.version[0])

# Create the downloads
create_download(cursor, 'macOS', args.version[0],
                'https://www.postgresql.org/ftp/pgadmin/pgadmin4/{0}/macos/',
                '')

create_download(cursor, 'Python', args.version[0],
                'https://www.postgresql.org/ftp/pgadmin/pgadmin4/{0}/pip/',
                '')

create_download(cursor, 'Source Code', args.version[0],
                'https://www.postgresql.org/ftp/pgadmin/pgadmin4/{0}/source/',
                'https://github.com/pgadmin-org/pgadmin4/blob/REL-{0}/README.md')

create_download(cursor, 'Windows', args.version[0],
                'https://www.postgresql.org/ftp/pgadmin/pgadmin4/{0}/windows/',
                '')
# Cleanup
conn.commit()
cursor.close()
conn.close()
