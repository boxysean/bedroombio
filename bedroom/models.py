from django.db import models

class Borough(models.Model):
  name = models.CharField(max_length=128)
  def __str__(self):
    return "%s" % (self.name)

class Neighborhood(models.Model):
  name = models.CharField(max_length=128)
  borough = models.ForeignKey(Borough)
  def __str__(self):
    return "%s" % (self.name)

class Bedroom(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  description = models.TextField()
  neighborhood = models.ForeignKey(Neighborhood)
  image = models.CharField(max_length=128)
  viewable = models.BooleanField()

  def __str__(self):
    return "%s: %s" % (self.neighborhood, self.description[0:min(30, len(self.description))])

class BedroomView(models.Model):
  visitTime = models.DateTimeField(auto_now_add=True)
  bedroom = models.ForeignKey(Bedroom)

