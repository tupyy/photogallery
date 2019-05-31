from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView, DetailView
from gallery.models import Album, AlbumAccessPolicy, Photo
from gallery.storages import get_storage

from PhotoGallery.forms.album_forms import AddAlbumForm


class AddAlbumCommonMixin(object):

    def album_exists(self, dirpath):
        _albums = Album.objects.filter(dirpath__exact=dirpath)
        return len(_albums) > 0

    def create_album(self, form):
        return Album.objects.create(category=form.cleaned_data['album_category'],
                                    dirpath=self.get_album_path(form),
                                    date=form.cleaned_data['album_date'],
                                    name=form.cleaned_data['album_name'])

    def get_album_path(self, form):
        return "{}/{}_{}_{}".format(form.cleaned_data['album_date'].year,
                                    self._pad_to_left(form.cleaned_data['album_date'].day),
                                    self._pad_to_left(form.cleaned_data['album_date'].month),
                                    form.cleaned_data['album_name'])

    def _pad_to_left(self, i):
        """Format date to string."""
        return '{0:02d}'.format(i)


class AddAlbumView(AddAlbumCommonMixin, FormView):
    template_name = 'photo_gallery/add_album.html'
    form_class = AddAlbumForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_label'] = "Add"
        return context

    def form_valid(self, form):
        if not self.album_exists(self.get_album_path(form)):
            _album = self.create_album(form)

            # add access policy for the created album
            access_policy = AlbumAccessPolicy.objects.create(album=_album)
            access_policy.users.add(self.request.user)
            for group in self.request.user.groups.all():
                access_policy.groups.add(group)
        else:
            context = self.get_context_data()
            context['form_error'] = "Album exists: {}".format(form.cleaned_data['album_name'])
            return self.render_to_response(context)
        return super().form_valid(form)


class DeleteAlbumView(DeleteView):
    model = Album
    success_url = reverse_lazy('index')
    template_name = 'photo_gallery/delete_album_confirmation.html'

    def post(self, request, *args, **kwargs):
        photo_storage = get_storage('photo')
        _, files = photo_storage.listdir(self.get_object().dirpath)
        for file in files:
            if file is not '.':
                photo_storage.delete(self.get_object().dirpath + "/" + file)
        photo_storage.delete(self.get_object().dirpath + '/')

        # delete caches
        # TODO implement delete caches
        return super().post(request, *args, **kwargs)
