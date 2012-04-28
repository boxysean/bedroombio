from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from forms import BedroomSubmitForm
from models import Bedroom, BedroomView, Neighborhood

import uuid, os, json, Image

import settings

import logging

logger = logging.getLogger(__name__)

def home(request):
  bedrooms = Bedroom.objects.all().order_by("-created")
  d = locals()
  d["bedrooms"] = bedrooms
  return render_to_response("home.html", d, context_instance=RequestContext(request))

def submit(request):
  neighborhoods = Neighborhood.objects.all().order_by("name")
  d = locals()
  d["neighborhoods"] = neighborhoods
  return render_to_response("submit.html", d, context_instance=RequestContext(request))

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
  except Exception, e:
    response_data["result"] = "fail"
    response_data["error"] = "Server error. Try again later."
    logger.error(e)
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
  
  raise Http404

def submit_bedroom(request):
  if request.method == "POST":
    response = {}
    form = BedroomSubmitForm(request.POST, request.FILES)

    required_fields = ["picture_file", "picture_crop_x", "picture_crop_y", "picture_crop_x2", "picture_crop_y2", "description", "neighborhood"]

    for rf in required_fields:
      if rf not in request.POST or len(request.POST[rf]) == 0:
        return HttpResponseRedirect("/submit/result?error=invalid_form")

    try:
      neighborhood = Neighborhood.objects.get(pk=int(request.POST["neighborhood"]))
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
        x2 = int(request.POST["picture_crop_x2"])
        y2 = int(request.POST["picture_crop_y2"])

        image = Image.open(os.path.join(settings.IMAGE_UPLOAD_FOLDER, filename))
        imw, imh = image.size

        imratio = 300.0 / imw # 300 is the width of the crop photo test

        x1p = x1 / imratio
        y1p = y1 / imratio
        x2p = x2 / imratio
        y2p = y2 / imratio

        if (x2p-x1p) < 600 or (y2p-y1p) < 400:
          return HttpResponseRedirect("/submit/result?error=cropping")

        image = image.crop((x1p, y1p, x2p, y2p))
        image = image.resize((600, 400), Image.ANTIALIAS) 
        image.save(os.path.join(settings.BEDROOM_PICTURE_FOLDER, "large", filename + ".jpg"))
        image = image.resize((220, 146), Image.ANTIALIAS) 
        image.save(os.path.join(settings.BEDROOM_PICTURE_FOLDER, "small", filename + ".jpg"))
  
        bedroom = Bedroom(description=description, neighborhood=neighborhood, image=filename + ".jpg", viewable=True)
        bedroom.save()
        return HttpResponseRedirect("/submit/result?success")
      else:
        logger.debug("fell through to here");
        return HttpResponseRedirect("/submit/result?error=invalid_form")
    except Exception, e:
      logger.error(e)
      return HttpResponseRedirect("/submit/result?error=server_error")
  
  return render_to_response("submission_result.html", locals(), context_instance=RequestContext(request))

def get_bedroom(request, bedroom_id):
  bedroom = Bedroom.objects.get(pk=bedroom_id)
  response_data = {"description": bedroom.description, "image": settings.STATIC_URL + "bedroom/large/" + bedroom.image, "neighborhood": bedroom.neighborhood.name}
  bedroomView = BedroomView(bedroom=bedroom)
  bedroomView.save()
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
    elif fail == "cropping":
      res["fail"] = "Please select a crop area."
    elif fail == "enter_desc":
      res["fail"] = "Please enter text into the response field."

  return render_to_response("submission_result.html", res, context_instance=RequestContext(request))


import sys
import traceback

from django.core.signals import got_request_exception

def exception_printer(sender, **kwargs):
    print >> sys.stderr, ''.join(traceback.format_exception(*sys.exc_info()))

got_request_exception.connect(exception_printer)

