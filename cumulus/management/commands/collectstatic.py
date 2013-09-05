import hashlib

from django.contrib.staticfiles.management.commands import collectstatic

from cumulus.storage import SwiftclientStaticStorage

class Command(collectstatic.Command):

    def delete_file(self, path, prefixed_path, source_storage):
        """
        Checks if the target file should be deleted if it already exists
        """
        dest_storage = self.storage
        if hasattr(self.storage, '_wrapped'):
            dest_storage = self.storage._wrapped

        if isinstance(dest_storage, SwiftclientStaticStorage):
            if self.storage.exists(prefixed_path):
                etag = self.storage._get_object(prefixed_path).etag
                digest = "{0}".format(hashlib.md5(source_storage.open(path).read()).hexdigest())
                if etag == digest:
                    self.log(u"Skipping '{0}' (not modified based on file hash)".format(path))
                    return False
                else:
                    self.log("Deleting '{0}'".format(path))
                    self.storage.delete(prefixed_path)
            return True

        return super(Command, self).delete_file(path, prefixed_path, source_storage)
