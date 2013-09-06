from django.contrib.staticfiles.management.commands import collectstatic

from cumulus.storage import CachingMixin

class Command(collectstatic.Command):

    def collect(self):
        """
        Enable and disable the bulk cache.
        """
        dest_storage = self.storage
        if hasattr(self.storage, '_wrapped'):
            dest_storage = self.storage._wrapped

        if isinstance(dest_storage, CachingMixin):
            self.storage._enable_bulk_cache()

        result = super(Command, self).collect()

        if isinstance(dest_storage, CachingMixin):
            self.storage._disable_bulk_cache()

        return result
