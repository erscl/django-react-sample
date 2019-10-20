from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from django.core.files import File
import os
import mimetypes

class ReactHostingView(View):
    def get(self, *args, **kwargs):
        target_file_path = os.path.join(settings.REACT_HOME, kwargs["path"])
        if not os.path.isfile(target_file_path):
            target_file_path = os.path.join(settings.REACT_HOME, "index.html")
        return HttpResponse(File(open(target_file_path, 'rb')), content_type=mimetypes.guess_type(target_file_path))
