from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import path
from .models import File
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class RocketFiles:
    """Rocket files application main view"""

    name = "rocket_files"

    def _get_urls(self):
        """Prepare application urls

        Returns:
            list -- application urls
        """

        urlpatterns = [
            path('push', self.binary_push, name="binary_push"),
            path('', self.index, name="index"),
        ]
        return urlpatterns

    @staticmethod
    def build_link(base, url):
        return "".join((base, url))

    @staticmethod
    def _save_file(filename, data):
        fullname = "/".join((settings.BASE_DIR, filename))
        try:
            with open(fullname, "wb+") as f:
                f.write(data)
        except Exception as e:
            logger.error("IO Error {}".format(e))
            return False
        return True

    @property
    def urls(self):
        return self._get_urls(), 'files', self.name

    def binary_push(self, request):
        """Handle uploading binary file

        Arguments:
            request {HttpRequest} -- incoming request which contents binary file in request body

        Returns:
            HttpResponse -- [description]
        """

        f = File()
        if request.method == "POST":
            f.file = "".join((settings.ROCKET_FILES_STORAGE, f.name))
            f.hash = request.META['HTTP_BODY_HASH']
            print(request.__dict__)
            #f.ttl = request.REQUEST['ttl']
            if self._save_file(str(f.file), request.body):
                f.save()
            else:
                return HttpResponse(status=500)
        return render(request, "push_success.j2", {
            'url': RocketFiles.build_link(settings.ROCKET_FILES_URL, f.get_absolute_link()),
            'file': f
            })

    def index(self, request):
        """"Handle `index` request

        Returns:
            HttpResponse -- content index page
        """

        return render(request, "index.j2", {'url': settings.ROCKET_FILES_URL})

rocket_files = RocketFiles()