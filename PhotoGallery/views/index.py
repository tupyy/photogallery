from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from gallery.views import GalleryIndexView


class PreviewCommonMixin(object):
    """ Provide can_add_album can_add_photo """

    def get_user_permissions(self):
        perms = {}
        if '_perm_cache' in self.request.user:
            for permission in self.request.user._perm_cache:
                perms[permission] = True
        return perms


class PreviewGalleryIndexView(PreviewCommonMixin, GalleryIndexView):

    def get_context_data(self, **kwargs):
        context = super(PreviewGalleryIndexView, self).get_context_data(**kwargs)
        albums = context['object_list']

        context['perms'] = self.get_user_permissions()

        preview_year = {}
        albums_count = getattr(settings, 'GALLERY_YEAR_PREVIEW', 5)
        for date in context['date_list']:
            album_year = [album for album in albums if album.date.year == date.year]
            sorted(album_year, key=lambda album: album.date)
            preview_year[date.year] = album_year[:albums_count]
        context['preview_year'] = preview_year

        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse('login_view'), args=(reverse('index')))
        return super().get(request, *args, **kwargs)
