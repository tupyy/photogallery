# Gallery settings
GALLERY_PHOTO_STORAGE = 'PhotoGallery.storages.photo'
GALLERY_YEAR_PREVIEW = 4
GALLERY_CACHE_STORAGE = 'PhotoGallery.storages.cache'

GALLERY_PATTERNS = (
    ('Photos',
        r'(?P<a_year>\d{4})\\(?P<a_month>\d{2})_(?P<a_day>\d{2})_'
        r'(?P<a_name>[^_/]+)\\'),
)

GALLERY_RESIZE_PRESETS = {
    'thumb': (256, 256, True),
    'standard': (768, 768, False),
}

GALLERY_RESIZE_OPTIONS = {
    'JPEG': {'quality': 95, 'optimize': True},
}

