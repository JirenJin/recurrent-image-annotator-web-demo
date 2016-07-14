from django.shortcuts import render
from django.http import JsonResponse

from .forms import UploadFileForm
from .utils import handle_uploaded_file

# Create your views here.
# One view is one page!
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = handle_uploaded_file(request.FILES['file'])
            return JsonResponse(result, safe=False)
    else:
        form = UploadFileForm()
    return render(request, 'annotator/index.html')
