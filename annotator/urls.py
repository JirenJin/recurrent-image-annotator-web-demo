from django.conf.urls import url

from . import views

app_name = 'annotator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^image_clicked$', views.image_clicked, name='image_clicked'),
]
