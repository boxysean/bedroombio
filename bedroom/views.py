from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from forms import BedroomSubmitForm
from models import Bedroom, ZipCode

import uuid, os, json, Image

import settings

import logging

logger = logging.getLogger(__name__)

def home(request):
  bedrooms = Bedroom.objects.all()
  return render_to_response("home.html", {"bedrooms": bedrooms}, context_instance=RequestContext(request))

def submit(request):
  return render_to_response("submit.html", locals(), context_instance=RequestContext(request))

def about(request):
  return render_to_response("about.html", locals(), context_instance=RequestContext(request))

def upload_picture(request):
  response_data = {}

  try:
    if request.method == 'POST':
      # TODO prevent many uploads in succession by the same person...
      f = request.FILES['picture']
      filename = str(uuid.uuid4())
      path = os.path.join(settings.IMAGE_UPLOAD_FOLDER, filename)
      destination = open(path, 'wb+')
      for chunk in f.chunks():
        destination.write(chunk)
      destination.close()
      
      # check dimensions
  
      image = Image.open(path)
      imw, imh = image.size
  
      if imw < 600 or imh < 400:
        response_data["result"] = "fail"
        response_data["error"] = "Images must be larger than 600x400"
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
  
      response_data["result"] = "success"
      response_data["file"] = filename
      return HttpResponse(json.dumps(response_data), mimetype="application/json")
  except:
    response_data["result"] = "fail"
    response_data["error"] = "Server Error. Try again later."
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
  
  raise Http404

def submit_bedroom(request):
  if request.method == "POST":
    response = {}
    form = BedroomSubmitForm(request.POST, request.FILES)

    required_fields = ["picture_file", "picture_crop_x", "picture_crop_y", "picture_crop_w", "picture_crop_h", "description", "zipcode"]

    for rf in required_fields:
      logger.debug(rf)
      if rf not in request.POST or len(request.POST[rf]) == 0:
        return HttpResponseRedirect("/submit/result?error=invalid_form")

    try:
      zipcode = ZipCode.objects.get(zipcode=int(request.POST["zipcode"]))
    except:
      return HttpResponseRedirect("/submit/result?error=nyc_only")

    description = request.POST["description"]

    if len(description) == 0:
      return HttpResponseRedirect("/submit/result?error=enter_desc")
    elif len(description) > 250:
      description = description[0:250]

    try:
      if form.is_valid():
        # resize it
  
        filename = request.POST["picture_file"]
        x1 = int(request.POST["picture_crop_x"])
        y1 = int(request.POST["picture_crop_y"])
        x2 = x1 + int(request.POST["picture_crop_w"])
        y2 = y1 + int(request.POST["picture_crop_h"])
        image = Image.open(os.path.join(settings.IMAGE_UPLOAD_FOLDER, filename))
        imw, imh = image.size
        image = image.resize((600, int(600.0 / imw * imh)), Image.ANTIALIAS)
        image = image.crop((x1, y1, x2, y2))
        image = image.resize((600, 400), Image.ANTIALIAS) 
        image.save(os.path.join(settings.BEDROOM_PICTURE_FOLDER, "large", filename + ".jpg"))
        image = image.resize((220, 146), Image.ANTIALIAS) 
        image.save(os.path.join(settings.BEDROOM_PICTURE_FOLDER, "small", filename + ".jpg"))
  
        bedroom = Bedroom(description=description, zipcode=zipcode, image=filename + ".jpg", viewable=True)
        bedroom.save()
        return HttpResponseRedirect("/submit/result?success")
      else:
        return HttpResponseRedirect("/submit/result?error=invalid_form")
    except:
      return HttpResponseRedirect("/submit/result?error=server_error")
  
  return render_to_response("submission_result.html", locals(), context_instance=RequestContext(request))

def get_bedroom(request, bedroom_id):
  bedroom = Bedroom.objects.get(pk=bedroom_id)
  response_data = {"description": bedroom.description, "image": settings.STATIC_URL + "bedroom/large/" + bedroom.image, "zipcode": bedroom.zipcode.__str__()}
  return HttpResponse(json.dumps(response_data), mimetype="application/json")

def get_bedroom_max_id(request):
  count = Bedroom.objects.all().count()
  response_data = {"maxId": count}
  return HttpResponse(json.dumps(response_data), mimetype="application/json")

def submit_result(request):
  res = {}

  if "success" in request.GET:
    res["success"] = "Submission complete."

  if "error" in request.GET:
    fail = request.GET["error"]
    if fail == "nyc_only":
      res["fail"] = "Bedroom Bio presently is only available for New York City."
    elif fail == "invalid_form":
      res["fail"] = "All fields are required."
    elif fail == "server_error":
      res["fail"] = "Server error. Please try again later."
    elif fail == "enter_desc":
      res["fail"] = "Please enter text into the response field."

  return render_to_response("submission_result.html", res, context_instance=RequestContext(request))


import sys
import traceback

from django.core.signals import got_request_exception

def exception_printer(sender, **kwargs):
    print >> sys.stderr, ''.join(traceback.format_exception(*sys.exc_info()))

got_request_exception.connect(exception_printer)

