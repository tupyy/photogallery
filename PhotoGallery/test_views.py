from __future__ import unicode_literals

import datetime
import tempfile

from django.contrib.auth.models import User,Permission
from django.test import TestCase
from django.urls import reverse

from gallery.models import Album,Photo
from gallery.test_views import ViewsTestsMixin


class ViewsTestGalleryPreviewIndex(ViewsTestsMixin, TestCase):

    def setUp(self):
        super(ViewsTestGalleryPreviewIndex,self).setUp()
        today = datetime.date.today()
        self.album = Album.objects.create(category='default', dirpath=self.tmpdir, date=today)
        self.photo = Photo.objects.create(album=self.album, filename='original.jpg')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.user_permissions.add(Permission.objects.get(codename='view'))
        self.client.login(username='user', password='pass')