import ipc
from .models import Image, Label, Annotation, Assign


def handle_uploaded_file(image_path):
    # database operation
    image, created = Image.objects.get_or_create(image=image_path)
    annotation, created = Annotation.objects.get_or_create(image=image, is_predicted=True)
    # get prediction result
    # important here to modify the image_path
    # note that the ipc server is running in 'annotator' directory instead of
    # the main project directory
    result = predict('../' + image_path)
    # add label objects, and assign labels to annotation 
    for word in result:
        label, created = Label.objects.get_or_create(label=word)
        assign, created = Assign.objects.get_or_create(annotation=annotation,
                label=label)
    return result

def predict(image_path):
    """Send image_path to ipc_server which is running forever for providing
    annotation results."""
    server_address = ('localhost', 5795)
    with ipc.Client(server_address) as client:
        result = client.send(image_path)
        # avoid duplicate labels in rare cases
        result = list(set(result))
    return result
