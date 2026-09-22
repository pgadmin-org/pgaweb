# pgaweb Tools

This directory contains various scripts used to manage www.pgadmin.org and pgAdmin downloads.

**Most are very system-specific; don't expect them to work for you!!**

On the production web server, all scripts **must** be run as the *pgaupload* user.

## create_release.py

This script is called as part of the release process, through the `create-release` verb of the publishing wrapper
(`pkg/publish/pga-publish` in the pgadmin4 repo) which the GitHub Actions workflows reach over SSH. It creates all the
required objects in the website database for a new release.

## load-docs.sh

This script is called as part of the release process, through the `load-docs` verb of the publishing wrapper. It
unpacks the docs for the version of pgAdmin specified on the command line, and loads them into the website database.

Because the tarball it unpacks is built elsewhere and lands in a tree that an upload key can write to, the script
treats it as untrusted input and vets the member list before unpacking anything; the comments in the script explain
what each check is there to stop.

## purge-cache.sh

This script is called as part of the release process, through the `purge-cache` verb of the publishing wrapper. It
purges the entire Varnish cache that sits in front of Nginx.

## update-docs.sh

This script is run from cron on the web server, twice an hour, as the *pgaupload* user, and is not part of the release
process. It updates the git checkout of pgAdmin at /var/www/pgaweb/static/docs/pgadmin4-dev, and then rebuilds the HTML
docs which are subsequently loaded into the website database as the 'dev' docs.
