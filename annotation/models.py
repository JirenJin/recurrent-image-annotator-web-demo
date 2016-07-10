from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Image(models.Model):
    """Each image contains multiple annotations."""
    # we need rename images after uploading
    # to ensure that image_path length is less than the maximum
    image_path = models.CharField(max_length=200)

    def __unicode__(self):
        return self.image_path 


class Label(models.Model):
    """Each label corresponds to multiple annotations."""
    # maximum length of english word is 45.
    label = models.CharField(max_length=50)

    def __unicode__(self):
        return self.label


class Annotation(models.Model):
    """Each annotation corresponds to one image.
       Each annotation contains multiple labels.    
       Each annotation is either predicted by RIA model or by humans.
    """
    # whether the annotation is predicted by RIA model
    # or annotated or corrected by humans
    is_predicted = models.BooleanField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    def __unicode__(self):
        return self.labels



