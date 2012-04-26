from django import forms

class UploadPictureForm(forms.Form):
  picture = forms.ImageField()

class BedroomSubmitForm(forms.Form):
  picture_crop_x = forms.IntegerField()
  picture_crop_y = forms.IntegerField()
  picture_crop_w = forms.IntegerField()
  picture_crop_h = forms.IntegerField()
  picture_file = forms.CharField()
  description = forms.CharField()
  zipcode = forms.IntegerField()

