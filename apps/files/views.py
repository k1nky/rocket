# Native
import logging
import os
# Django
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import path
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Home brew
from .models import File
from .helper import *


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
            path('push', self.push, name="push"),
            path('get/<str:filename>', self.get_file, name="get_file"),
            path('', self.index, name="index"),
        ]
        return urlpatterns

    def prepare_download_response(self, filename):
        """Prepare HttpResponse object on a download request

        Arguments:
            filename {str} -- requested file name

        Raises:
            Http404: specified file does not exist

        Returns:
            HttpRequest -- prepared response
        """
        fullname = build_storage_path(filename)
        if os.path.exists(fullname):
            try:
                with open(fullname, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = "inline;filename={}".format(filename)
                    return response
            except OSError as e:
                logger.error("{}", e)
                raise Http404("Specified file does not exist")

        return HttpResponse(status=500)


    @property
    def urls(self):
        """Processed urls by the application

        Returns:
            [list] -- list of django.urls.path
        """
        return self._get_urls(), 'files', self.name

    @permit_methods(("POST"))
    def push(self, request):
        """Handle uploading file

        Arguments:
            request {HttpRequest} -- incoming request which contents binary file in request body

        Returns:
            HttpResponse -- [description]
        """

        f = File()
        f.file = f.name
        f.hash = request.META['HTTP_BODY_HASH']
        f.ttl = request.GET['ttl']

        if save_file(str(f.file), request.body):
            f.save()
        else:
            return HttpResponse(status=500)

        return render(request, "push_success.j2", {
            'url': build_link(f.get_absolute_link()),
            'file': model_to_dict(f, fields=[fld.name for fld in f._meta.fields])
            })

    @permit_methods(('GET', 'POST'))
    def index(self, request):
        """"Handle `index` request

        Arguments:
            request {HttpRequest} -- incoming request
        Returns:
            HttpResponse -- content index page
        """

        return render(request, "index.j2", {'url': settings.ROCKET_FILES_URL})

    @permit_methods(('GET', 'POST'))
    def get_file(self, request, filename):
        """Handle download requests

        Arguments:
            request {HttpRequest} -- incoming request
            filename {str} -- requested file name

        Raises:
            Http404: specified file does not exist

        Returns:
            HttpResponse -- response which body contains binary data
        """
        try:
            f = File.objects.get(name=filename)
        except ObjectDoesNotExist as e :
            raise Http404("Specified file does not exist")
        except MultipleObjectsReturned as e:
            logger.error("File {} duplication is detected {}".format(filename, e))
            raise Http404("Specified file does not exist")

        return self.prepare_download_response(filename)

rocket_files = RocketFiles()