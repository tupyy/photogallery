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

    def delete_objects(self, objects, quit_mode=False):
        delete_dict = {'Objects': [],
                       'Quiet': quit_mode}
        if isinstance(objects, list):
            for _object in objects:
                if isinstance(_object, dict):
                    delete_dict.get('Objects').append({'Key': _object.key,
                                                       'VersionId': _object.versionId})
                else:
                    delete_dict.get('Objects').append({'Key': _object})
        return self.get_bucket().delete_objects(Delete=delete_dict,
                                                RequestPayer='requester')

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
        key = key[:-1] if key.endswith('/') else key
        key = key + '/' + filename
        self.s3.Object(self.get_bucket().name, key).upload_file(file)


class AWSCommonMixin(AWSBase):
    """Class to provide photos and albums operation in a bucket"""

    def __init__(self):
        super().__init__()

    def delete_album(self, album_name):
        files_to_delete = self.get_objects(album_name)
        files_to_delete.append(album_name)
        response = self.delete_objects(files_to_delete)
