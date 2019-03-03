from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from PhotoGallery import settings
from PhotoGallery.views.upload_photo import UploadView
from authentication.views import login_view, logout_view

from PhotoGallery.views.index import PreviewGalleryIndexView

"""
    Url patterns for account
"""
urlpatterns_account = [
    url(r'^accounts/login/', login_view, name='login_view'),
    url(r'^accounts/logout/', logout_view, name='logout_view'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns = [
    path('', PreviewGalleryIndexView.as_view(), name='index'),
    path('upload', UploadView.as_view(), name='photo-upload'),
    path('', include('gallery.urls', namespace='gallery')),
]

urlpatterns += urlpatterns_account

if settings.ENV == 'development' or settings.ENV == 'development_aws':
    urlpatterns += [url(r'^admin/', admin.site.urls)]
