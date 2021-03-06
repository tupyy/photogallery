# -*- coding: utf-8 -*-
import os

from PhotoGallery.settings.components.database import DATABASES_DEV

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = "my_super_secret_key"
DEFAULT_FILE_STORAGE = 'PhotoGallery.storage.PhotoS3Boto3'
MEDIA_ROOT = "/photos/"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

"""
    Load variables from config.env
"""
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
baseconf = os.path.join(basedir, 'config.env')
if os.path.exists(baseconf):
    print('Importing environment from .env file {}'.format(os.path.abspath(baseconf)))
    for line in open(baseconf):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0].strip()] = var[1].strip().replace("\"", "")

"""
AWS S3 Storage settings
"""
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = None

DATABASES = DATABASES_DEV

S3_URL = 'https://{0}.s3.amazonaws.com'.format(os.getenv('AWS_STORAGE_BUCKET_NAME'))
MEDIA_URL = S3_URL + "/photos/"
