import json
import os
import logging
from datetime import datetime

import boto3
from botocore.config import Config
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView
from gallery.models import Album, Photo

logger = logging.getLogger('django')


class AlbumUploadPhotoView(DetailView):
    """
    This class is used to get the upload view and to handle post request after the upload to s3 has been completed
    """
    model = Album
    template_name = 'upload/upload_form.html'

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        album = self.get_object()
        logger.info('successful upload: ' + data.get('filename'))

        filename = data.get('filename')
        if not Photo.objects.filter(Q(album__name__exact=album.name), Q(filename__exact=filename)).exists():
            Photo.objects.create(album=album, filename=data.get('filename'), date=datetime.now())

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

        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': 'photos/' + album.dirpath + '/' + data.get('filename'),
                'ContentType': data.get('filetype')
            }
        )
        # Return the data to the client
        return JsonResponse({'url': presigned_url})
