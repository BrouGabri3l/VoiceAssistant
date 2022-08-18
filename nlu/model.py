import yaml
import numpy
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
data = yaml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())

inputs, outputs = [], []
for command in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append('{}\{}'.format(command['entity'], command['action']))
# processar texto
chars = set()
for inp in inputs + outputs:
    for ch in inp:
        if ch not in chars:
            chars.add(ch)

# mapear chars > index
chr2indx = {}
idx2chr = {}
for i, ch in enumerate(chars):
    chr2indx[ch] = i
    idx2chr[i] = ch

# max_seq = max([len(bytes(x.encode('utf-8'))) for x in inputs])
max_seq = 48
print('Maior sequencia:', max_seq)
# dataset (num exemplos, tamanho da seq, num de chars )one-hot

input_data = numpy.zeros((len(inputs), max_seq, 256), dtype='float32')
for i, inp in enumerate(inputs):
    for k, ch in enumerate(bytes(inp.encode('utf-8'))):
        input_data[i, k, int(ch)] = 1.0
# output_data = to_categorical(output_data, len(output_data))
print(input_data[0].shape)
labels = set(outputs)
fwrite = open('nlu\entities.txt', 'w', encoding='utf-8')
for label in labels:
    fwrite.write(label + "\n")
fwrite.close()
labels = open('nlu\entities.txt', 'r', encoding='utf-8').read().split('\n')
label2idx = {}
idx2lbl = {}
for k, label in enumerate(labels):
    label2idx[label] = k
    idx2lbl[k] = label
output_data = []
for output in outputs:
    output_data.append(label2idx[output])
output_data = to_categorical(output_data, len(labels))
model = Sequential([
    LSTM(128),
    Dense(len(labels), activation='softmax')
])
model.compile(optimizer='adam',
              loss='categorical_crossentropy', metrics=['acc'])
model.fit(input_data, output_data, epochs=256)

model.save('nlu\models\model.h5')



def classify(text):
    x = numpy.zeros((1, max_seq, 256), dtype='float32')
    for k, ch in enumerate(bytes(text.encode('utf-8'))):
        x[0, k, int(ch)] = 1.0
    out = model.predict(x)
    idx = out.argmax()
    # print('Texto: "{}" classificado como "{}"'.format(text, idx2lbl[idx]))
    return idx2lbl[idx]


# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()
# with open('nlu\\tflitemodel.tflite', 'wb') as f:
#     f.write(tflite_model)
