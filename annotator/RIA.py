import chainer
from chainer import Variable
import chainer.links as L
import chainer.functions as F


class VGGNet(chainer.Chain):
    """
    VGGNet
    - input: (N, 3, 224, 224)
    """

    def __init__(self):
        super(VGGNet, self).__init__(
            conv1_1=L.Convolution2D(3, 64, 3, stride=1, pad=1),
            conv1_2=L.Convolution2D(64, 64, 3, stride=1, pad=1),

            conv2_1=L.Convolution2D(64, 128, 3, stride=1, pad=1),
            conv2_2=L.Convolution2D(128, 128, 3, stride=1, pad=1),

            conv3_1=L.Convolution2D(128, 256, 3, stride=1, pad=1),
            conv3_2=L.Convolution2D(256, 256, 3, stride=1, pad=1),
            conv3_3=L.Convolution2D(256, 256, 3, stride=1, pad=1),

            conv4_1=L.Convolution2D(256, 512, 3, stride=1, pad=1),
            conv4_2=L.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv4_3=L.Convolution2D(512, 512, 3, stride=1, pad=1),

            conv5_1=L.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv5_2=L.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv5_3=L.Convolution2D(512, 512, 3, stride=1, pad=1),

            fc6=L.Linear(25088, 4096),
            fc7=L.Linear(4096, 4096),
            fc8=L.Linear(4096, 1000)
        )

    def __call__(self, x, t):
        """Forward pass computation, without saving computation history.
        return: 4096 dimension image features (fc7 features)
        """
        # set volatile to "on", then the computation history will not be stored 
        # we only need forward computation for deploying the trained model
        x.volatile = 'on'

        h = F.relu(self.conv1_1(x))
        h = F.relu(self.conv1_2(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv2_1(h))
        h = F.relu(self.conv2_2(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv3_1(h))
        h = F.relu(self.conv3_2(h))
        h = F.relu(self.conv3_3(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv4_1(h))
        h = F.relu(self.conv4_2(h))
        h = F.relu(self.conv4_3(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv5_1(h))
        h = F.relu(self.conv5_2(h))
        h = F.relu(self.conv5_3(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.dropout(F.relu(self.fc6(h)), train=self.train, ratio=0.5)
        h = F.dropout(F.relu(self.fc7(h)), train=self.train, ratio=0.5)
        # we only need the fc7 layer's output, i.e., 4096-D features
        return h


class RIA(chainer.Chain):
    def __init__(self):
        super(RIA, self).__init__(
            embed=L.EmbedID(261, 512),
            lstm=L.LSTM(512, 512, forget_bias_init=1.0),
            fc1=L.Linear(512, 512),
            fc2=L.Linear(512, 261),
            image_embedding = L.Linear(4096, 512),
        )

    def reset_state(self):
        self.lstm.reset_state()

    def initialize_state(self, image_features):
        # no training
        image_features.volatile="on"
        h = self.image_embedding(image_features)
        self.lstm.h = h

    def __call__(self, label_input):
        # no training
        label_input.volatile="on"
        x = self.embed(label_input)
        h = self.lstm(x)
        y = F.relu(self.fc1(h))
        logit = self.fc2(y)
        return logit
