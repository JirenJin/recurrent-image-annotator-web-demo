import datetime

from .models import Image, Label, Annotation, Assign


def handle_uploaded_file(f):
    image_ext = f.name.split('.')[1]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    file_path = 'annotator/uploaded_images/'
    file_name = file_path + timestamp + '.' + image_ext
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # database operation
    image = Image.objects.create(image=file_name)
    annotation = Annotation.objects.create(image=image, is_predicted=True)
    # get prediction result
    result = predict(file_name)
    # add label objects, and assign labels to annotation 
    for word in result:
        label, created = Label.objects.get_or_create(label=word)
        assign, created = Assign.objects.get_or_create(annotation=annotation,
                label=label)
    return result

def predict(image):
    # fake function
    annotation = ['dog', 'cat', 'grass', 'human']
    return annotation
