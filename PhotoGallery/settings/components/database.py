# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
import os

from PhotoGallery.settings.utils.utils import parse_db_variable

DATABASES_DEV = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'photos',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

db_variables = parse_db_variable(os.environ.get('DATABASE_URL'))
DATABASES_AWS = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_variables[4],
        'USER': db_variables[0],
        'PASSWORD': db_variables[1],
        'HOST': db_variables[2],
        'PORT': db_variables[3]
    }
}

