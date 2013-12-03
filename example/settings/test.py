from common import *  # noqa

INSTALLED_APPS += (
    'cumulus.tests',
    'example.photos',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'integration.db',              # Or path to database file if using sqlite3.
    }
}
