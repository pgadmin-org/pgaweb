PGAdmin Website

# Installation instructions

## Install Python dependencies
Run the command:

```bash
pip install -r requirements.txt
```

## Create local settings file
Create a the file pgaweb/settings_local.py from pgaweb/settings.py changing the needed options to run locally.
For connection complaints inquiring about postgres "running locally and accepting connections on Unix domain socket...",
you'll need to change the `HOST` from the postgres data directory to `localhost`.


## Database setup

### Create a new database

Create a new database using the command

```bash
createdb pgaweb
```

### Create Migrations for individual modules
```bash
./manager.py makemigrations download
./manager.py makemigrations faq
./manager.py makemigrations news
./manager.py makemigrations versions
```

### Migrate database

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

## Install frontend requirements

```bash
pushd static
yarn install
popd
```

# Start the application

```bash
./manage.py runserver
```

# WSGI Deployment

The server will automatically compile SCSS files at startup. If you're running behind (for example) uWSGI, you may
need to manually create the static/COMPILED directory and ensure it has the correct permissions/ownership to allow
updates to be made at startup.