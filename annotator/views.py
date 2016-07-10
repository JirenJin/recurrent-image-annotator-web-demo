from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.
def index(request):
    # add some fake data to be displayed
    annotation = ["bird", "sea", "sky", "cloud"]
    context = {
            'annotation': annotation,
            }
    return render(request, 'annotator/index.html', context)
