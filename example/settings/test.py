from common import *  # noqa

INSTALLED_APPS += (
    'example.photos',
    'example.things',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'integration.db',              # Or path to database file if using sqlite3.
    }
}
