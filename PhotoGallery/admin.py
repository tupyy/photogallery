from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from gallery.admin import AlbumAdmin
from gallery.models import Album, Photo
from gallery.storages import get_storage


class MyAlbumAdmin(AlbumAdmin):
    actions = ['clean_album']

    def clean_album(self, request, queryset):
        album = queryset[0]
        photos = Photo.objects.filter(album_id__exact=album.id)
        photo_storage = get_storage('photo')
        cache_storage = get_storage('cache')

        counter = 0
        for photo in photos:
            if not photo_storage.exists(photo.album.dirpath + "/" + photo.filename):
                # check if cache exists, delete it also
                if cache_storage.exists(photo.thumb_name('thumb')):
                    cache_storage.delete(photo.thumb_name('thumb'))
                photo.delete()
                counter += 1

        alert_message = "{} photos are not present on storage and they have been deleted".format(counter) \
            if counter > 0 else "The album is already clean"
        self.message_user(request, alert_message, messages.SUCCESS)
        return HttpResponseRedirect(request.path_info)


admin.site.unregister(Album)
admin.site.register(Album, MyAlbumAdmin)
