pgAdmin Website
===============

# Installation instructions

## Prerequisites

* Python 3 (CI uses 3.13).
* A PostgreSQL server that you can create roles and databases on.
* Node.js 24, which is what CI builds with. Newer releases have been reported
  to leave puppeteer's copy of Chrome unextracted after `npm ci`, which breaks
  the critical css step of the build.

## Install Python dependencies
Run the command:

```bash
pip install -r requirements.txt
```

## Database setup

### Create a role and database

The site connects as the `pgaweb` role, so create it and give it ownership of
the database. Since PostgreSQL 15 only the database owner can create tables in
the `public` schema by default, so `migrate` will fail with `permission denied
for schema public` if the database belongs to some other role.

```bash
createuser -P pgaweb
createdb -O pgaweb pgaweb
```

## Create local settings file

`pgaweb/settings.py` imports `pgaweb/settings_local.py` at the end, if it
exists, so the local file only needs the settings you want to override; do not
copy the whole of `settings.py`. The defaults connect over the Unix socket in
`/var/run/postgresql`, which uses peer authentication on most Linux
distributions and so only works if your operating system user is also called
`pgaweb`. Otherwise, connect over TCP with the password set above:

```python
DATABASES = {
    'default': {
        'ENGINE': 'pgaweb.db',
        'NAME': 'pgaweb',
        'USER': 'pgaweb',
        'PASSWORD': 'the password you gave createuser',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

### Migrate database

The migrations are committed to the repository, so there is no need to run
`makemigrations`.

```bash
./manage.py migrate
```

### Populate the table

You will at least need to:

```bash
./manage.py loaddata ./versions/fixtures/versions.json
```

If you want to see the other content in the site running locally,
you will need to repeat this for the other fixtures:

```bash
./manage.py loaddata ./download/fixtures/packages.json
./manage.py loaddata ./download/fixtures/distributions.json
./manage.py loaddata ./download/fixtures/versions.json
./manage.py loaddata ./download/fixtures/downloads.json
./manage.py loaddata ./faq/fixtures/categories.json
./manage.py loaddata ./faq/fixtures/faqs.json
./manage.py loaddata ./news/fixtures/news.json
```

# Front end build dependencies

The build generates critical css using a copy of Chrome that puppeteer
downloads during `npm ci`, and Chrome needs a number of shared libraries that
a server or minimal install may not have. On Debian 13, and Ubuntu 24.04 or
later, install:

```
apt-get install ca-certificates fonts-liberation libasound2t64 \
  libatk-bridge2.0-0t64 libatk1.0-0t64 libatspi2.0-0t64 libc6 libcairo2 \
  libcups2t64 libdbus-1-3 libexpat1 libgcc-s1 libgdk-pixbuf-2.0-0 \
  libglib2.0-0t64 libgtk-3-0t64 libnspr4 libnss3 libpango-1.0-0 \
  libpangocairo-1.0-0 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
  libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \
  libxss1 libxtst6
```

A desktop install usually has all of these except `libxss1`. On any other
distribution, run `npm ci` first and then list what is missing with:

```bash
ldd node_modules/puppeteer/.local-chromium/*/chrome-linux/chrome | grep "not found"
```

If Chrome cannot start, the build still succeeds and the site still renders
correctly, but with the complete stylesheet in place of the critical css, so
check the build output for a `Critical css generation FAILED` warning.

# Run the build

```bash
npm ci
npm run build
```

# Start the application

```bash
./manage.py runserver
```

# WSGI Deployment

The server will automatically compile SCSS files at startup. If you're running behind (for example) uWSGI, you may
need to manually create the static/COMPILED directory and ensure it has the correct permissions/ownership to allow
updates to be made at startup.
