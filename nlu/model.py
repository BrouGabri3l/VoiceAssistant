import yaml
import numpy
data = yaml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())
inputs, outputs = [], []
for command in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append('{}\{}'.format(command['entity'], command['action']))
# processar texto
chars = set()
for input in inputs + outputs:
    for ch in input:
        if ch not in chars:
            chars.add(ch)

# mapear chars > index
chr2indx = {}
idx2chr = {}
for i, ch in enumerate(chars):
    chr2indx[ch] = i
    idx2chr[i] = ch

max_seq = max([len(x) for x in inputs])
print('Maior sequencia:', max_seq)
# dataset (num exemplos, tamanho da seq, num de chars )one-hot

input_data = numpy.zeros((len(inputs), max_seq, len(chars)), dtype='int32')
for i, input in enumerate(inputs):
    for k, ch in enumerate(input):
        input_data[i, k, chr2indx[ch]] = 1.0
print(input_data[0])
# print(inputs)
# print(outputs)
