from django import forms
from PIL import Image

from django.core.exceptions import ValidationError

class BedroomSubmitForm(forms.Form):
  picture_crop_x = forms.IntegerField()
  picture_crop_y = forms.IntegerField()
  picture_crop_x2 = forms.IntegerField()
  picture_crop_y2 = forms.IntegerField()
  picture_file = forms.CharField()
  description = forms.CharField()
  neighborhood = forms.IntegerField()

