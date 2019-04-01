import json

import boto3
from botocore.config import Config
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from gallery.models import Album


class AlbumUploadPhotoView(TemplateView):
    template_name = 'upload/upload_form.html'


class AlbumSignS3View(DetailView):
    model = Album

    def post(self, *args, **kwargs):
        # Load necessary information into the application
        S3_BUCKET = "cosmin-photos-test"

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
