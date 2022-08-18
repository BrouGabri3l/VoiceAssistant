import numpy
import json
import requests
labels = open('nlu\entities.txt', 'r', encoding='utf-8').read().split('\n')

label2idx = {}
idx2lbl = {}
for k, label in enumerate(labels):
    label2idx[label] = k
    idx2lbl[k] = label


def classify_text(text):
    x = numpy.zeros((1, 48, 256), dtype='float32')

    if len(text) > 48:
        text = text[:48]
    for k, ch in enumerate(bytes(text.encode('utf-8'))):
        x[0, k, int(ch)] = 1.0
    datax = x.tolist()
    data = {
        "instances": datax}
    dumped = json.dumps(data)
    headers = {"content-type": "application/json"}
    json_response = requests.post(
        'https://heroku-docker-tf.herokuapp.com/v1/models/savedmodels:predict', data=dumped, headers=headers)
    predictions = json.loads(json_response.text)["predictions"]
    refine = max(predictions)
    tmp = max(refine)
    idx = refine.index(tmp)
    print('Texto: "{}" classificado como "{}"'.format(text, idx2lbl[idx]))
    return(idx2lbl[idx])


if __name__ == '__main__':
    text = input('coloque algum texto:')
    print(classify_text(text))
