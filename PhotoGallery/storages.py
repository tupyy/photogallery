from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class PhotoS3Boto3(S3Boto3Storage):
    location = 'photos'


def photo():
    if settings.ENV == 'development':
        return FileSystemStorage(location='G:\\AmazonAWS\\photos')
    return S3Boto3Storage(location='photos')


def cache():
    if settings.ENV == 'development':
        return FileSystemStorage(location='G:\\AmazonAWS\\caches')
    return S3Boto3Storage(location='caches')


