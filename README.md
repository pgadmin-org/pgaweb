pgAdmin Website
===============

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



# Dependencies

In order for yarn build to run successfully for generating critical css on 
Debian or Centos systems, additional libraries need to be installed on the 
system. Please install the dependencies below on respective systems.

For CentOS:

```
yum install alsa-lib atk cups-libs GConf2 gtk3 ipa-gothic-fonts libXcomposite \
  libXcursor libXdamage libXext libXi libXrandr libXScrnSaver libXtst pango \
  xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-fonts-cyrillic \
  xorg-x11-fonts-misc xorg-x11-fonts-Type1 xorg-x11-utils
```

For Debian:

```
apt-get install ca-certificates fonts-liberation gconf-service \
  libappindicator1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 \
  libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libgconf-2-4 \
  libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
  libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
  libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \
  libxss1 libxtst6 lsb-release wget xdg-utils
```

# Run the build

```bash
yarn install
yarn run build
```

# Start the application

```bash
./manage.py runserver
```

# WSGI Deployment

The server will automatically compile SCSS files at startup. If you're running behind (for example) uWSGI, you may
need to manually create the static/COMPILED directory and ensure it has the correct permissions/ownership to allow
updates to be made at startup.