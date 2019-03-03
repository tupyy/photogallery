# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

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

