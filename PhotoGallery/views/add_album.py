from django.views.generic import FormView

from PhotoGallery.forms.add_album_form import AddAlbumForm


class AddAlbumView(FormView):
    template_name = 'photo_gallery/add_album.html'
    form_class = AddAlbumForm
    success_url = '/'

    def form_valid(self, form):
        # TODO create album
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_label'] = "Add"
        return self.render_to_response(context)
