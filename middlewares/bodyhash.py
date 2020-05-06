import hashlib
from django.conf import settings

class BodyHash:
    """ Retrieve hash for a request body """

    def __init__(self, get_response):
        self.get_response = get_response

        self.algo = "md5"
        if hasattr(settings, 'BODYHASH_ALGO'):
            self.algo = settings.BODYHASH_ALGO

    def _get_hash(self, data):
        # TODO add exception catching
        h = hashlib.new(self.algo)
        h.update(data)
        return h.hexdigest()

    def __call__(self, request):

        request.META["HTTP_BODY_HASH"] = self._get_hash(request.body)
        response = self.get_response(request)

        return response
