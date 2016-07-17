import os
import datetime 
import random

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
        context = {}
        num_sample_image = 4
        # this view will be called from the site main directory
        parent_dicrectory = "annotator/static/annotator/iaprtc12/"
        rand = random.choice(range(4))
        if rand == 0:
            parent_dicrectory += "h320/"
        elif rand == 1:
            parent_dicrectory += "h360/"
        elif rand == 2:
            parent_dicrectory += "w320/"
        else:
            parent_dicrectory += "w360/"
        image_list = random.sample(os.listdir(parent_dicrectory),
                                   num_sample_image)
        # this path will be used in Django `static` template tag, thus we omit
        # 'annotator/static/'
        sample_image_paths = [parent_dicrectory.replace('annotator/static/', '') + image_name 
                              for image_name in image_list]
        context['sample_image_paths'] = sample_image_paths
    return render(request, 'annotator/index.html', context)


def image_clicked(request):
    image_path = request.POST['image_path']
    # modify the path
    image_path = 'annotator/static/' + image_path
    result = handle_uploaded_file(image_path)
    return JsonResponse(result, safe=False)    
