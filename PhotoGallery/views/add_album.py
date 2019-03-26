from django.views.generic import FormView

from PhotoGallery.forms.add_album_form import AddAlbumForm


class AddAlbumView(FormView):
    template_name = 'photo_gallery/add_album.html'
    form_class = AddAlbumForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid()