import hashlib
import mimetypes
from gzip import GzipFile
from StringIO import StringIO

from django.core.files.base import ContentFile

def get_digest(content):
    """Get the MD5 has of the content, suitable for use as the etag"""
    return "{0}".format(hashlib.md5(content).hexdigest())

def gzip_content(content):
    """Returns a gzipped version of a previously opened file's buffer."""
    zbuf = StringIO()
    zfile = GzipFile(mode="wb", compresslevel=6, fileobj=zbuf)
    zfile.write(content.read())
    zfile.close()
    return ContentFile(zbuf.getvalue())

def read_gzipped_content(content):
    zbuf = StringIO(content)
    zfile = GzipFile(mode="rb", fileobj=zbuf)
    return zfile.read()

def get_content_type(content, name):
    """
    Checks if the content_type is already set. Otherwise uses the mimetypes
    library to guess.
    """
    if hasattr(content.file, "content_type"):
        return content.file.content_type
    else:
        mime_type, encoding = mimetypes.guess_type(name)
        return mime_type
