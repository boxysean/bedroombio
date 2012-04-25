from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from forms import UploadPictureForm

import logging

logger = logging.getLogger(__name__)

def home(request):
  return render_to_response("home.html", locals() , context_instance=RequestContext(request))

def submit(request):
  return render_to_response("submit.html", locals() , context_instance=RequestContext(request))

def about(request):
  return render_to_response("about.html", locals() , context_instance=RequestContext(request))

def upload_picture(request):
  logger.debug("yes!0")
  if request.method == 'POST':
    # TODO prevent many uploads in succession by the same person...
    try:
      logger.debug("post: " + request.POST.__str__())
      logger.debug("files: " + request.FILES.__str__())
      form = UploadPictureForm(request.POST, request.FILES)
    except Exception as e:
      logger.debug(e)
    if form.is_valid():
      f = request.FILES['picture']
      destination = open('/tmp/' + f.name, 'wb+')
      for chunk in f.chunks():
        destination.write(chunk)
      destination.close()
      return render_to_response("upload_picture_response.html", {"response": "success!"})
    else:
      logger.debug("yes!-2")
      return render_to_response('upload_picture_response.html', {"response": "invalid form"})
  raise Http404

