# recurrent-image-annotator-web-demo
Web demo for recurrent image annotator: http://arxiv.org/abs/1604.05225

# Installation
- python 2.7
- django
- postgresql

```bash
sudo apt-get install postgresql postgresql-contrib
```
- psycopg2: necessary to install libpq-dev and python-dev 

```bash
# for ubuntu
sudo apt-get install libpq-dev python-dev
pip install psycopg2
sudo apt-get install apache2-mpm-worker
sudo apt-get install apache2-threaded-dev
```

# Start ipc server
```bash
python ipc_server.py
```

## The `annotator` app
### models
- Image: store the relative paths of images.
- Label: store the keyword in the annotation vocabulary.
- Annotation: Each annotation corresponds to one image, and contains multiple labels.
- Assign: Connect the labels to a specific annotation of an image.

### views
- index: display the page content, receive the image uploading request, and return the annotation result as response.
- image_clicked: receive the request with the corresponding image path, and return the annotation result as response.
