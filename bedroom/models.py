from django.db import models

#from django.db.models.signals import post_save

# Create your models here.

class ZipCode(models.Model):
  borough = models.CharField(max_length=128)
  zipcode = models.IntegerField()

  def __str__(self):
    return "%d" % (self.zipcode)

class Bedroom(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  description = models.TextField()
  zipcode = models.ForeignKey(ZipCode)
  image = models.CharField(max_length=128)
  viewable = models.BooleanField()

  def __str__(self):
    return "%05d: %s" % (self.zipcode, self.description[0:min(30, len(self.description))])


