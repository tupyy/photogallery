from __future__ import unicode_literals

from django.conf import settings
from gallery.views import GalleryIndexView


class PreviewCommonMixin(object):
    """ Provide can_add_album can_add_photo """
    def can_add_album(self):
        return self.request.user.has_perm('gallery.add_album')

    def can_add_photo(self):
        return self.request.user.has_perm('gallery.add_photo')


class PreviewGalleryIndexView(PreviewCommonMixin, GalleryIndexView):

    def get_context_data(self, **kwargs):
        context = super(PreviewGalleryIndexView,self).get_context_data(**kwargs)
        albums = context['object_list']

        if self.can_add_album():
            context['can_add_album'] = True

        preview_year = {}
        albums_count = getattr(settings, 'GALLERY_YEAR_PREVIEW', 5)
        for date in context['date_list']:
            album_year = [album for album in albums if album.date.year == date.year]
            sorted(album_year, key=lambda album: album.date)
            preview_year[date.year] = album_year[:albums_count]
        context['preview_year'] = preview_year

        return context