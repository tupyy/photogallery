from django.views.generic import TemplateView


class UploadView(TemplateView):
    template_name = 'upload/upload_form.html'
