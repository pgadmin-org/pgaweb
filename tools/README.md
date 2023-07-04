# pgaweb Tools

This directory contains various scripts used to manage www.pgadmin.org and pgAdmin downloads.

**Most are very system-specific; don't expect them to work for you!!**

**Note:** The AWS CLI is expected to be installed at /usr/bin/aws.

Om the production web server, all scripts **must** be run as the *pgaupload* user.

## create-release.py

This script is called by the Jenkins server as part of the release process. It creates all the required objects in the
website database for a new release.

## load-docs.sh

This script is called by the Jenkins server as part of the release process. It unpacks the docs for the version of
pgAdmin specified on the command line, and loads them into the website database.

## purge-cache.sh

This script is called by the Jenkins server as part of the release process. It purges the entire Varnish cache that 
sits in front of Nginx.

# rebuild-apt-repo.sh

This script will rebuild the specified APT repo metadata, and re-sign everything. This is typically used if old 
packages are manually removed.

```bash
./rebuild-apt-repo.sh focal
```

# rebuild-yum-repo.sh

This script will rebuild the specified YUM repo metadata, and re-sign everything. This is typically used if old 
packages are manually removed.

```bash
./rebuild-yum-repo.sh redhat rhel 8
```

## sync-ftp-to-s3.py

This script is called by the Jenkins server as part of the release process. It will copy all the packages to the S3 
bucket that hosts https://pgadmin-archive.postgresql.org, and generate and sync HTML index pages for browsing.

## update-docs.sh

This script is typically called from cron. It updates the git checkout of pgAdmin at 
/var/www/pgaweb/static/docs/pgadmin4-dev, and then rebuilds the HTML docs which are subsequently loaded into the 
website database as the 'dev' docs.
