# -*- coding: utf-8 -*-

"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""
import os

from PhotoGallery.settings.utils.utils import parse_db_variable

DEBUG = False
ALLOWED_HOSTS = ['cosmin-photos.herokuapp.com']
SECRET_KEY = os.getenv('SECRET_KEY')

CORS_ORIGIN_WHITELIST = (
    's3.amazonaws.com',
    'cosmin-photos.herokuapp.com'
)
"""
Database Postgres for Heroku
"""
db_variables = parse_db_variable(os.environ.get('DATABASE_URL'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_variables[4],
        'USER': db_variables[0],
        'PASSWORD': db_variables[1],
        'HOST': db_variables[2],
        'PORT': db_variables[3]
    }
}

"""
AWS S3 Storage settings
"""
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

MEDIA_ROOT = "/photos/"
S3_URL = 'https://{0}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = S3_URL + "/photos/"
DEFAULT_FILE_STORAGE = 'PhotoGallery.storage.PhotoS3Boto3'

#white noise
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




