from django.shortcuts import redirect
from django.views.generic import DeleteView

from gallery.models import Photo
from gallery.storages import get_storage


class DeletePhotoView(DeleteView):
    model = Photo
    template_name = 'photo_gallery/delete_photo_confirmation.html'

    def post(self, request, *args, **kwargs):
        photo = self.get_object()
        album_id = photo.album.id

        photo_storage = get_storage('photo')
        cache_storage = get_storage('cache')

        photo_storage.delete(photo.album.dirpath + "/" + photo.filename)
        cache_storage.delete(photo.thumbnail('thumb'))

        photo.delete()
        return redirect('/album/{}'.format(album_id))
