import json

import ipc
import deploy


def server_process_request(image_path):
    try:
        # note that we have to explicitly pass the params to predict function
        annotation = deploy.predict(image_path, vgg, ria, dictionary)
    except KeyError:
        annotation = []
    return annotation 


if __name__ == '__main__':
    server_address = ('localhost', 5795)

    dataset = 'iaprtc12'

    print 'Start loading models and dictionary, please wait for about 10 seconds'
    with open(dataset + '_dictionary.json') as f:
        dictionary = json.load(f)

    vgg, ria = deploy.load_models(dataset + '_RIA.model', len(dictionary), 1024, 1024)

    print 'Model Loading completed'
    print 'Ready for annotating'

    ipc.Server(server_address, server_process_request).serve_forever()
