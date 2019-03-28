from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from PhotoGallery import settings
from PhotoGallery.views.album import AddAlbumView, DeleteAlbumView
from PhotoGallery.views.upload_photo import UploadView, SignS3View
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
    path('add_album', AddAlbumView.as_view(), name="add_album_view"),
    path('delete_album/<pk>', DeleteAlbumView.as_view(), name='delete_album_view'),
    path('upload', UploadView.as_view(), name='photo-upload'),
    path('sign-s3', SignS3View.as_view(), name='sign-s3'),
    path('', include('gallery.urls', namespace='gallery')),
]

urlpatterns += urlpatterns_account

if settings.ENV == 'development' or settings.ENV == 'development_aws':
    urlpatterns += [url(r'^admin/', admin.site.urls)]
