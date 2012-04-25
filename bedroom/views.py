from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
#from django.http import HttpResponse, HttpResponseRedirect

def home(request):
  return render_to_response("home.html", locals() , context_instance=RequestContext(request))

def submit(request):
  return render_to_response("submit.html", locals() , context_instance=RequestContext(request))

def about(request):
  return render_to_response("about.html", locals() , context_instance=RequestContext(request))

