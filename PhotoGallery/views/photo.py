from django.views.generic import DetailView

from gallery.models import Photo
from gallery.storages import get_storage


class DeletePhotoView(DetailView):
    model = Photo

    def post(self):
        photo = self.get_object()

        photo_storage = get_storage('photo')
        cache_storage = get_storage('cache')

        photo_storage.delete(photo.album.dirpath + "/" + photo.filename)
        cache_storage.delete(photo.thumbnail('thumb'))

        photo.delete()
