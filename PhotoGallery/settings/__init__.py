# -*- coding: utf-8 -*-

"""
wemake-django-template

This is a django-split-settings main file.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from os import environ

from split_settings.tools import include

# Managing environment via DJANGO_ENV variable:
environ.setdefault('DJANGO_ENV', 'development_aws')
ENV = environ['DJANGO_ENV']


base_settings = [
    'components/logging.py',
    'components/common.py',
    'components/gallery.py',
    'components/database.py',

    # You can even use glob:
    # 'components/*.py'

    # Select the right env:
    'environments/{0}.py'.format(ENV),

]


# Include settings:
include(*base_settings)