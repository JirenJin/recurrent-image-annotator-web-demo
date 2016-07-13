import json

import numpy as np
import cv2
import chainer

from RIA import VGGNet, RIA


# load pretrained VGG and RIA models
def load_models():
    """Load both trained VGG and RIA models"""
    vgg = VGGNet()
    chainer.serializers.load_hdf5('VGG.model', vgg)
    vgg.to_gpu()

    ria = RIA()
    chainer.serializers.load_npz('RIA.model', ria)
    ria.to_gpu()
    return vgg, ria


def get_image_features(image_path):
    """Load an image and extract the image features.""" 
    # training images pixel mean
    mean = np.array([103.939, 116.779, 123.68])
    img = cv2.imread(image_path).astype(np.float32)
    img -= mean
    # [224, 224, 3] to [3, 224, 224]
    img = cv2.resize(img, (224, 224)).transpose((2, 0, 1))
    # input for VGGNet should be [1, 3, 224, 224]
    img = img[np.newaxis, :, :, :]
    img = chainer.cuda.cupy.asarray(img, dtype=np.float32)
    image_features = vgg(img)
    return image_features


def predict(image_path):
    """Predict the multi-label annotation for the given image.
    To-do:
        implement beam-search for better result, however, this may casue more
        computation time.
    """
    # load image
    image_features = get_image_features(image_path)
    # initialize hidden state
    ria.reset_state()
    ria.initialize_state(image_features)
    # START signal, here it's [0] with shape (1,)
    label_init = chainer.cuda.cupy.zeros([1], dtype=np.int32)
    # output has shape (1,dictionary_size + 1) 
    output = ria(label_init)
    # so pred has shape (1,1)
    pred = output.data.argmax(1)
    # number of predicted labels
    i = 0
    # list of predicted labels
    preds = []
    # maximum length for annotation
    max_length = 5

    # continue predicting until STOP signal (also 0) is predicted
    # or the number of predicted labels exceeds the maximum
    # here 5 is the maximum limit for Corel5k dataset
    # however, it is OK to not set this in practice
    # since all the training examples have annotation length less than 5,
    # the learned model probably only learned how to predict labels within this
    # limit
    # thus later I prefer to replace the current model with another one that
    # trained on another dataset that has more number of labels, 
    # e.g., IAPRTC-12
    while(pred[0] != 0 and i < max_length):
        preds.append(pred[0])
        # use the previous predicted label as the next input to RIA model
        label_input = pred.astype(np.int32)
        output = ria(label_input)
        pred = output.data.argmax(1)
        i += 1

    # annotation with multiple label word
    annotation = [dictionary[int(pred)] for pred in preds]
    return annotation



# simple test
if __name__ == "__main__":
    # load trained models
    vgg, ria = load_models()

    # label dictionary
    with open('dictionary.json') as f:
        dictionary = json.load(f)

    annotation = predict('cat.jpg')
    print " ".join(annotation)
