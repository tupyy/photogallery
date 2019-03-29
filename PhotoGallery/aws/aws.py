import os

import boto3
import botocore


class AWSBase(object):
    BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

    def __init__(self):
        self.s3 = boto3.resource('s3')

    def has_bucket(self, bucket_name):
        exists = True
        try:
            self.s3.meta.client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
        return exists

    def get_bucket(self, bucket_name=BUCKET_NAME):
        if not self.has_bucket(bucket_name):
            raise AttributeError('Bucket \'{}\' don\'t exists'.format(bucket_name))
        return self.s3.bucket(bucket_name)

    def delete_objects(self, objects, quit_mode=False):
        delete_dict = {'Objects': [],
                       'Quite': quit_mode}
        if isinstance(objects, list):
            for _object in objects:
                if isinstance(_object, dict):
                    delete_dict.get('Objects').append({'Key': _object.key,
                                                       'VersionId': _object.versionId})
                else:
                    delete_dict.get('Objects').append({'Key': _object})
        return self.s3.get_bucket().delete_objects(Delete=delete_dict,
                                                   RequestPayer='requester')

    def get_objects(self, key):
        """Return a list with all the objects under the key"""
        objects = []
        for _object in self.s3.get_bucket().objects.all():
            if _object.starswith(key):
                objects.append(_object)
        return objects

    def upload_file(self, key, file):
        if not key:
            raise AttributeError('Key is empty.')

        if not os.path.isfile(file):
            raise AttributeError('File not exits.')

        self.s3.get_bucket().upload_file(file, key)


class AWSCommonMixin(AWSBase):
    """Class to provide photos and albums operation in a bucket"""

    def __init__(self):
        super().__init__()

    def delete_album(self, album_name):
        files_to_delete = self.get_objects(album_name)
        files_to_delete.append(album_name)
        response = self.delete_objects(files_to_delete)

