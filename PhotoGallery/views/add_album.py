from django.views.generic import FormView
from gallery.models import Album

from PhotoGallery.forms.add_album_form import AddAlbumForm


class AddAlbumCommonMixin(object):

    def album_exists(self, dirpath):
        _album = Album.objects.filter(dirpath__exact=dirpath)
        return len(_album) > 0

    def create_album(self, form):
        Album.objects.create(category=form.cleaned_data['album_category'],
                             dirpath=self.get_album_path(form),
                             date=form.cleaned_data['album_date'],
                             name=form.cleaned_data['album_name'])

    def get_album_path(self, form):
        return "{}\\{}_{}_{}".format(form.cleaned_data['album_date'].year,
                                     self._pad_to_left(form.cleaned_data['album_date'].day),
                                     self._pad_to_left(form.cleaned_data['album_date'].month),
                                     form.cleaned_data['album_name'])

    def _pad_to_left(self, i):
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
            self.create_album(form)
        else:
            context = self.get_context_data()
            context['form_error'] = "Album exists: {}".format(form.cleaned_data['album_name'])
            return self.render_to_response(context)
        return super().form_valid(form)
