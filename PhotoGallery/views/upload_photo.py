import os
import boto3
from botocore.config import Config

from PhotoGallery import settings

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


class UploadView(TemplateView):
    template_name = 'upload/upload_form.html'


class SignS3View(View):
    def get(self, *args, **kwargs):
        # Load necessary information into the application
        S3_BUCKET = "cosmin-photos-test"

        # Load required data from the request
        file_name = self.request.GET.get('file-name')
        file_type = self.request.GET.get('file-type')

        # Initialise the S3 client
        s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': file_name,
                'ContentType': file_type
            }
        )

        # Return the data to the client
        return JsonResponse({
            'presigned_url': presigned_url
        })
