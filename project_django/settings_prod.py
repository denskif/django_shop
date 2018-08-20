DEBUG = False
ALLOWED_HOSTS = ['*']

# settings for db on server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_shop',
        'USER': 'denskif',
        'PASSWORD': '80931207152qw',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}