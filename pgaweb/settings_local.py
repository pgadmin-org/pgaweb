DEBUG=True

SESSION_COOKIE_SECURE=False
SESSION_COOKIE_DOMAIN=None
CSRF_COOKIE_SECURE=False
CSRF_COOKIE_DOMAIN=None

DATABASES={
        'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'pgaweb',
                'USER': 'pgaweb',
                'PASSWORD': 'pgaweb',
                'HOST': '/tmp',
                'PORT': 5434
                }
        }

ALLOWED_HOSTS = ['wwwdevel.pgadmin.org',]