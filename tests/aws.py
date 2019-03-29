import os
import tempfile
import unittest

from binascii import hexlify

from PhotoGallery.aws.aws import AWSBase


class AWSTests(unittest.TestCase):

    def setUp(self) -> None:
        self.load_aws_credentials()
        self.bucket_name = 'cosmin-test-{}'.format(hexlify(os.urandom(24)).decode('utf-8')[6:])
        os.environ['S3_BUCKET_NAME'] = self.bucket_name

        self.aws = AWSBase()
        self.bucket = self.aws.s3.Bucket(self.bucket_name)
        response = self.bucket.create(ACL='private',
                                      CreateBucketConfiguration={
                                          'LocationConstraint': 'EU'
                                      })
        if response.get('Location') is None:
            raise ValueError('Cannot create test bucket')

    def tearDown(self) -> None:
        for key in self.bucket.objects.all():
            key.delete()
        self.bucket.delete()

    def test_list_files(self):
        file = self.create_temporary_file('testfile.txt')
        self.aws.upload_file('test_folder', file)
        files = self.aws.get_objects('test_folder')
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], os.path.basename(file))

    def test_delete_file(self):
        file = self.create_temporary_file('testfile.txt')
        self.aws.upload_file('test_folder', file)
        files = self.aws.get_objects('test_folder')

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], os.path.basename(file))

        self.aws.delete_objects(['test_folder/testfile.txt'])
        files = self.aws.get_objects('test_folder')
        self.assertEqual(len(files), 0)

    def create_temporary_file(self, filename):
        tmp_folder = tempfile.gettempdir()
        with open(os.path.join(tmp_folder, filename), 'a') as f:
            f.write('Test line')
        return os.path.join(tmp_folder, filename)

    def load_aws_credentials(self):
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        baseconf = os.path.join(basedir, 'config.env')
        if os.path.exists(baseconf):
            print('Importing environment from .env file {}'.format(os.path.abspath(baseconf)))
            for line in open(baseconf):
                var = line.strip().split('=')
                if len(var) == 2:
                    os.environ[var[0].strip()] = var[1].strip().replace("\"", "")
