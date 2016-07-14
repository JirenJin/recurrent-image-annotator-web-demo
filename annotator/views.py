import datetime

from django.shortcuts import render
from django.http import JsonResponse

from .forms import UploadFileForm
from .utils import handle_uploaded_file

# Create your views here.
# One view is one page!
# pwd is the main project directory!
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            image_ext = f.name.split('.')[1]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            path_pre = 'annotator/uploaded_images/'
            image_path = path_pre + timestamp + '.' + image_ext
            with open(image_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            result = handle_uploaded_file(image_path)
            return JsonResponse(result, safe=False)
    else:
        form = UploadFileForm()
    return render(request, 'annotator/index.html')


def image_clicked(request):
    image_path = request.POST['image_path']
    # modify the path
    image_path = 'annotator/static/' + image_path
    result = handle_uploaded_file(image_path)
    return JsonResponse(result, safe=False)    
