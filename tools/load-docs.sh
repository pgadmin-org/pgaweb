#!/bin/bash

if [ $# -ne 1 ]
then
  echo "usage: $0 <version number>"
  exit 1
fi

# Check the docs file exists
TARBALL=/var/ftp/pgadmin4/v${1}/docs/pgadmin4-${1}-docs.tar.gz
if [ ! -f ${TARBALL} ]
then
  echo "The source tarball (${TARBALL}) could not be found."
  exit 1
fi

# Unpack the tarball
cd /var/www/pgaweb/static/docs
tar -zxvf ${TARBALL}

# Load 'em
cd /var/www/pgaweb
source /usr/share/python3/pginfra-virtualenv-django42-py3/bin/activate
./manage.py docloader pgadmin4 ${1} pgadmin4-${1}-docs

# Clear the cache
sudo varnishadm "ban req.url ~ ."
