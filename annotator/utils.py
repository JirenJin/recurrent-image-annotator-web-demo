import datetime

from .models import Image, Label, Annotation, Assign


def handle_uploaded_file(f):
    image_ext = f.name.split('.')[1]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    file_path = 'annotator/uploaded_images/'
    file_name = file_path + timestamp + image_ext
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    image = Image.objects.create(image=file_name)
