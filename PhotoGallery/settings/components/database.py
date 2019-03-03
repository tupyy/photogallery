# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
import os
from PhotoGallery.settings.components import BASE_DIR

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

