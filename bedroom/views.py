from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from forms import UploadPictureForm, BedroomSubmitForm

import uuid, os, json

import settings

import logging

logger = logging.getLogger(__name__)

def home(request):
  return render_to_response("home.html", locals() , context_instance=RequestContext(request))

def submit(request):
  return render_to_response("submit.html", locals() , context_instance=RequestContext(request))

def about(request):
  return render_to_response("about.html", locals() , context_instance=RequestContext(request))

def upload_picture(request):
  response_data = {}

  if request.method == 'POST':
    # TODO prevent many uploads in succession by the same person...
    form = UploadPictureForm(request.POST, request.FILES)
    if form.is_valid():
      f = request.FILES['picture']
      logger.debug(f)
      logger.debug(dir(f))
      filename = str(uuid.uuid4())
      path = os.path.join(settings.IMAGE_UPLOAD_FOLDER, filename)
      destination = open(os.path.join(settings.IMAGE_UPLOAD_FOLDER, filename), 'wb+')
      for chunk in f.chunks():
        destination.write(chunk)
      destination.close()
      response_data["result"] = "success!"
      response_data["file"] = filename
      return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
      response_data["result"] = "invalid form!"
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

  raise Http404

def submit_bedroom(request):
  if request.method == "POST":
    form = BedroomSubmitForm(request.POST, request.FILES)
    logger.debug(request.POST);
    if form.is_valid():
      logger.debug("valid form");
      # TODO crop photo
      # TODO add bedroom to database
    else:
      logger.debug("invalid form");

  raise Http404



import sys
import traceback

from django.core.signals import got_request_exception

def exception_printer(sender, **kwargs):
    print >> sys.stderr, ''.join(traceback.format_exception(*sys.exc_info()))

got_request_exception.connect(exception_printer)

