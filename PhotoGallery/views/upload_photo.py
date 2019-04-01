import json
import os
from datetime import datetime

import boto3
from botocore.config import Config
from django.http import JsonResponse
from django.views.generic import DetailView
from gallery.models import Album, Photo


class AlbumUploadPhotoView(DetailView):
    """
    This class is used to get the upload view and to handle post request after the upload to s3 has been completed
    """
    model = Album
    template_name = 'upload/upload_form.html'

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        album = self.get_object()

        for uploadedPhoto in data.get('done'):
            Photo.objects.create(album=album, filename=uploadedPhoto, date=datetime.now())
        return JsonResponse({'status': 'ok'})


class AlbumSignS3View(DetailView):
    """
    View for signing the files to be upload to s3
    """
    model = Album

    def post(self, *args, **kwargs):
        # Load necessary information into the application
        S3_BUCKET = os.getenv('S3_BUCKET_NAME', 'cosmin-photos')

        album = self.get_object()

        # Load required data from the request
        data = json.loads(self.request.body.decode('utf-8'))

        # Initialise the S3 client
        s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

        signed_urls = dict()
        for k, v in data.items():
            presigned_url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': S3_BUCKET,
                    'Key': 'photos/' + album.dirpath + '/' + v.get('filename'),
                    'ContentType': v.get('filetype')
                }
            )
            signed_urls[k] = presigned_url

        # Return the data to the client
        return JsonResponse(signed_urls)
