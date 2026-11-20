pgAdmin Website
===============

# Installation instructions

## Prerequisites

* Python 3 (CI uses 3.13).
* A PostgreSQL server that you can create roles and databases on.
* Node.js 22.13 or later, which the critical css step of the build requires.
  CI builds with Node.js 24.

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

# Run the build

The critical css step no longer needs a browser. If it fails, the build still
succeeds and the site still renders correctly, but with the complete
stylesheet in place of the critical css, so check the build output for a
`Critical css generation FAILED` warning.

```bash
npm ci
npm run build
```

## Adding images

The build copies `static/img/*` and `static/img/screenshots/` into
`static/COMPILED/assets/img/` as they are, without compressing them, so
compress a new or changed image before committing it, for example with:

```bash
pngquant --quality=0-50 --skip-if-larger --force --ext .png image.png
jpegtran -copy none -optimize -outfile out.jpg image.jpg
npx svgo image.svg
```

Leave `static/img/bimi.svg` alone: it must stay in the SVG Tiny PS profile
that BIMI requires, and `svgo` strips its `<title>`.

# Start the application

```bash
./manage.py runserver
```

# WSGI Deployment

The server will automatically compile SCSS files at startup. If you're running behind (for example) uWSGI, you may
need to manually create the static/COMPILED directory and ensure it has the correct permissions/ownership to allow
updates to be made at startup.
