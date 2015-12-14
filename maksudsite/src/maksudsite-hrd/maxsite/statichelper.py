from apps.bloggart.lib import aetycoon
from google.appengine.api import memcache
from google.appengine.ext import db
import hashlib

class StaticContent(db.Model):
    """Container for statically served content.

      The serving path for content is provided in the key name.
    """
#    body = db.BlobProperty(required=True)
    body = db.BlobProperty(required=True)
    content_type = db.StringProperty(required=True)
    last_modified = db.DateTimeProperty(required=True, auto_now=True)
    etag = aetycoon.DerivedProperty(lambda x: hashlib.sha1(x.body).hexdigest())
    


def get_static_content(path):
    """Returns the StaticContent object for the provided path.

  Args:
    path: The path to retrieve StaticContent for.
  Returns:
    A StaticContent object, or None if no content exists for this path.
    """
    return StaticContent.get_by_key_name(path)


def set_static_content(path, body, content_type, ** kwargs):
    """Sets the StaticContent for the provided path.

  Args:
    path: The path to store the content against.
    body: The data to serve for that path.
    content_type: The MIME type to serve the content as.
    **kwargs: Additional arguments to be passed to the StaticContent constructor
  Returns:
    A StaticContent object.
    """
    content = StaticContent(
                            key_name=path,
                            body=body,
                            content_type=content_type,
                            ** kwargs)
    content.put()
    return content