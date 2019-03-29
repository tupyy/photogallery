import json
import os
import boto3
from botocore.config import Config

from PhotoGallery import settings

from django.http import JsonResponse, HttpResponseServerError
from django.views import View
from django.views.generic import TemplateView


class UploadView(TemplateView):
    template_name = 'upload/upload_form.html'


class SignS3View(View):
    def post(self, *args, **kwargs):
        # Load necessary information into the application
        S3_BUCKET = "cosmin-photos-test"

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
                    'Key': v.get('filename'),
                    'ContentType': v.get('filetype')
                }
            )
            signed_urls[k] = presigned_url

        # Return the data to the client
        return JsonResponse(signed_urls)
