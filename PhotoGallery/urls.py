from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from PhotoGallery import settings
from PhotoGallery.views.album import AddAlbumView, DeleteAlbumView
from PhotoGallery.views.upload_photo import AlbumSignS3View, AlbumUploadPhotoView
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

"""
    Url patterns for album
"""
urlpatterns_album = [
    path('album/create', AddAlbumView.as_view(), name="add_album_view"),
    path('album/delete/<pk>', DeleteAlbumView.as_view(), name='delete_album_view'),
    path('album/sign-s3/<pk>', AlbumSignS3View.as_view(), name='sign-s3'),
    path('album/upload/<pk>', AlbumUploadPhotoView.as_view(), name='photo-upload')
]

urlpatterns = [
    path('', PreviewGalleryIndexView.as_view(), name='index'),
    path('', include('gallery.urls', namespace='gallery')),
]

urlpatterns += urlpatterns_account
urlpatterns += urlpatterns_album

urlpatterns += [url(r'^admin/', admin.site.urls)]
