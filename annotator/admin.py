from django.contrib import admin

# Register your models here.
from .models import Image, Label, Annotation, Assign

admin.site.register(Image)
admin.site.register(Label)
admin.site.register(Annotation)
admin.site.register(Assign)
