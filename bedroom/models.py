from django.db import models

#from django.db.models.signals import post_save

# Create your models here.

class Bedroom(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  description = models.TextField()
  zipcode = models.IntegerField()
  image = models.ImageField()
  viewable = models.BooleanField()

#  def __str__(self):
#    return "%05d: %s" % (self.zipcode, self.description)
