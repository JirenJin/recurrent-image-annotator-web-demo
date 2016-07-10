from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Image(models.Model):
    """Each image contains multiple annotations."""
    # we need rename images after uploading
    # to ensure that image_path length is less than the maximum
    image = models.CharField(max_length=200, primary_key=True)

    def __unicode__(self):
        return "%s" % self.image


class Label(models.Model):
    """Each label corresponds to multiple annotations."""
    # maximum length of english word is 45
    label = models.CharField(max_length=50, primary_key=True)

    def __unicode__(self):
        return "%s" % self.label


class Annotation(models.Model):
    """Each annotation corresponds to one image.
       Each annotation contains multiple labels.    
       Each annotation is either predicted by RIA model or by humans.
    """
    # whether the annotation is predicted by RIA model
    # or annotated or corrected by humans
    is_predicted = models.BooleanField()
    # use 'image' instead of Django's default 'image_id' for ForeignKey,
    # since we directly use 'image' as the primary key 
    image = models.ForeignKey(Image, on_delete=models.CASCADE, db_column='image')
    # use 'Assign' as an intermediate model
    labels = models.ManyToManyField(Label, through='Assign')

    def __unicode__(self):
        return " ".join(l.label for l in self.labels.all())


class Assign(models.Model):
    """Assign a label to an annotation result of an image."""
    annotation = models.ForeignKey(Label, on_delete=models.CASCADE,
            db_column='label')
    label = models.ForeignKey(Annotation, on_delete=models.CASCADE,
            db_column='annotation')

    class Meta:
        db_table = Image._meta.app_label + '_label_link_annotation'
