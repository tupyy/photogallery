from __future__ import unicode_literals

from sesame.utils import get_query_string
from django.contrib.auth.models import User
from django.core.management import base


class Command(base.BaseCommand):
    help = "Generate auth token for users."

    def add_arguments(self, parser):
        parser.add_argument (
            'user_name'
        )

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username__exact=options['user_name'])
            auth_link = get_query_string(user)
            self.stdout.write(auth_link)
        except User.DoesNotExist:
            self.stdout.write("User don't exits.")
