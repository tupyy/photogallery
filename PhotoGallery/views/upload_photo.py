import os
import boto3
from django.conf import settings

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


class UploadView(TemplateView):
    template_name = 'upload/upload_form.html'


class SignS3View(View):
    def get(self, *args, **kwargs):
        # Load necessary information into the application
        S3_BUCKET = os.environ.get('S3_BUCKET')

        # Load required data from the request
        file_name = self.request.GET.get('file-name')
        file_type = self.request.GET.get('file-type')

        # Initialise the S3 client
        s3 = boto3.client('s3')

        # Generate and return the presigned URL
        presigned_post = s3.generate_presigned_post(
            Bucket=getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
            Key=file_name,
            Fields={"acl": "bucket-owner-full-control", "Content-Type": file_type},
            Conditions=[
                {"acl": "bucket-owner-full-control"},
                {"Content-Type": file_type},
                {"Access-Control-Allow-Origin": "*"}
            ],
            ExpiresIn=3600
        )

        # Return the data to the client
        return JsonResponse({
            'data': presigned_post,
            'url': 'https://%s.s3.amazonaws.com/%s' % (getattr(settings, 'AWS_STORAGE_BUCKET_NAME'), file_name)
        })
