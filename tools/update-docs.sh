#!/bin/bash

set -e

# Update the GIT repo
cd /var/www/pgaweb/static/docs/pgadmin4-dev
git reset --hard
git pull

# Update the venv
source /var/www/pgadocs/venv/bin/activate && pip3 install -r requirements.txt sphinx sphinxcontrib-youtube

# Build the docs
cd docs/en_US
PYTHONWARNINGS= make -f Makefile.sphinx PYTHON=/var/www/pgadocs/venv/bin/python SPHINXBUILD=/var/www/pgadocs/venv/bin/sphinx-build html

# Run the docloader
cd /var/www/pgaweb
source /usr/share/python3/pginfra-virtualenv-django32-py3/bin/activate
./manage.py docloader pgadmin4 Development pgadmin4-dev/docs/en_US/_build/html

