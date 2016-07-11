from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from .models import Image, Label, Annotation, Assign

from .utils import handle_uploaded_file

# Create your views here.
# One view is one page!
def index(request):
    # add some fake data to be displayed
    annotation = ["bird", "sea", "sky", "cloud"]
    context = {
            'annotation': annotation,
            }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            #return HttpResponseRedirect(reverse('annotator:index', args={}))
    else:
        form = UploadFileForm()
    return render(request, 'annotator/index.html', context)
