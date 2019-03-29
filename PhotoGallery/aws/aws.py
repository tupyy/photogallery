import os

import boto3
import botocore


class AWSBase(object):

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

    def get_bucket(self, bucket_name=None):
        if not bucket_name:
            bucket_name = os.getenv('S3_BUCKET_NAME')
        if not self.has_bucket(bucket_name):
            raise AttributeError('Bucket \'{}\' don\'t exists'.format(bucket_name))
        return self.s3.Bucket(bucket_name)

    def delete_objects(self, objects, quiet_mode=False):
        delete_dict = {'Objects': [],
                       'Quiet': quiet_mode}
        if isinstance(objects, list):
            for _object in objects:
                if isinstance(_object, dict):
                    delete_dict.get('Objects').append({'Key': _object.key,
                                                       'VersionId': _object.versionId})
                else:
                    delete_dict.get('Objects').append({'Key': _object})
        response = self.get_bucket().delete_objects(Delete=delete_dict,
                                                    RequestPayer='requester')
        return 'Error' not in response, response.get('Error', None)

    def get_objects(self, key):
        """Return a list with all the objects under the key
            if file is under key1/key2/filename returns key2/filename
        """
        objects = []
        for _object in self.get_bucket().objects.all():
            metadata = _object.key.split('/')
            if metadata[0] == key:
                objects.append(''.join(metadata[1:]))
        return objects

    def upload_file(self, key, file):
        if not key:
            raise AttributeError('Key is empty.')

        if not os.path.isfile(file):
            raise AttributeError('File not exits.')

        filename = os.path.basename(file)
        key = self.clean_key(key) + '/' + filename
        self.s3.Object(self.get_bucket().name, key).upload_file(file)

    def clean_key(self, key):
        """Remove the / at the end if any"""
        return key[:-1] if key.endswith('/') else key


class AWSCommon(AWSBase):
    """Class to provide photos and albums operation in a bucket"""

    def __init__(self):
        super().__init__()

    def delete_album(self, album):
        files = self.get_objects(album)
        keys = [self.clean_key(album) + '/' + file for file in files]
        keys.append(album)
        return self.delete_objects(keys)

    def delete_photo(self, album, photo):
        return self.delete_objects(album + '/' + photo)
