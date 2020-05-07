# native
import os
import logging
# django
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseNotAllowed

__all__ = ['permit_methods', 'save_file', 'build_link', 'build_storage_path']

logger = logging.getLogger(__name__)

def permit_methods(methods):
    """ Decorator checks that a request method is permitted.

    Arguments:
        methods {tuple} -- list of allowed methods
    """
    def outer_decorator(func):

        def inner_decorator(self, request, *args, **kwargs):

            if len(methods) != 0 and request.method not in methods:
                return HttpResponseNotAllowed(methods)

            return func(self, request, *args, **kwargs)

        return inner_decorator

    return outer_decorator

def save_file(filename, data):
    """Save a file as binary to application storage

    Arguments:
        filename {str} -- file name
        data {AnyStr} -- saved data

    Returns:
        bool -- True if saving is successful, else False
    """
    fullname = build_storage_path(filename)
    try:
        with open(fullname, "wb+") as f:
            f.write(data)
    except Exception as e:
        logger.error("IO Error {}".format(e))
        return False
    return True

def build_link(url):
    """Simple join `url` with base application url

    """
    return "".join((settings.ROCKET_FILES_URL, url))

def build_storage_path(filename):
    """Build absolute path for specified filename in the storage

    Arguments:
        filename {str} -- file name within the storage

    Returns:
        str -- full path for specified file
    """
    return os.path.join(settings.BASE_DIR, settings.ROCKET_FILES_STORAGE, filename)
