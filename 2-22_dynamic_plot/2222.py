import numpy as np
import os
import time
import matplotlib.pyplot as plt
import tensorflow as tf
import re
import urllib.request
import zipfile
import lxml.etree
from collections import Counter
from random import shuffle
from gensim.models import KeyedVectors

# Download the dataset if it's not already there
if not os.path.isfile('ted_en-20160408.zip'):
    urllib.request.urlretrieve(
        "https://wit3.fbk.eu/get.php?path=XML_releases/xml/ted_en-20160408.zip&filename=ted_en-20160408.zip",
        filename="ted_en-20160408.zip")

# extract both the texts and the labels from the xml file
with zipfile.ZipFile('ted_en-20160408.zip', 'r') as z:
    doc = lxml.etree.parse(z.open('ted_en-20160408.xml', 'r'))
texts = doc.xpath('//content/text()')
labels = doc.xpath('//head/keywords/text()')
del doc

print("There are {} input texts, each a long string with text and punctuation.".format(len(texts)))
print("")
print(texts[0][:100])

# method remove unused words and labels
inputs_text = [re.sub(r'\([^)]*\)', ' ', text) for text in texts]
inputs_text = [re.sub(r':', ' ', text) for text in inputs_text]
# inputs_text = [text.split() for text in inputs_text]
print(inputs_text[0][0:100])

inputs_text = [text.lower() for text in texts]
inputs_text = [re.sub(r'([^a-z0-9\s])', r' <\1_token> ', text) for text in inputs_text]
# input_texts = [re.sub(r'([^a-z0-9\s])', r' <\1_token> ', input_text) for input_text in input_texts]
inputs_text = [text.split() for text in inputs_text]
print(inputs_text[0][0:100])

# label procession
label_lookup = ['ooo', 'Too', 'oEo', 'ooD', 'TEo', 'ToD', 'oED', 'TED']
new_label = []
for i in range(len(labels)):
    labels_pre = ['o', 'o', 'o']
    label = labels[i].split(', ')
    # print(label,i)
    if 'technology' in label:
        labels_pre[0] = 'T'
    if 'entertainment' in label:
        labels_pre[1] = 'E'
    if 'design' in label:
        labels_pre[2] = 'D'
    labels_temp = ''.join(labels_pre)
    label_index = label_lookup.index(labels_temp)
    new_label.append(label_index)

print('the length of labels:{0}'.format(len(new_label)))
print(new_label[0:50])
labels_index = np.zeros((len(new_label), 8))
# for i in range(labels_index.shape[0]):
#  labels_index[i,new_label[i]] = 1
labels_index[range(len(new_label)), new_label] = 1.0
print(labels_index[0:10])

# feature selections
unions = list(zip(inputs_text, labels_index))
unions = [union for union in unions if len(union[0]) > 300]
print(len(unions))
inputs_text, labels_index = zip(*unions)
inputs_text = list(inputs_text)
labels = list(labels_index)
print(inputs_text[0][0:50])
print(labels_index[0:10])

# feature filttering

all_context = [word for text in inputs_text for word in text]
print('the present datas word is :{0}'.format(len(all_context)))
words_count = Counter(all_context)
most_words = [word for word, count in words_count.most_common(50)]
once_words = [word for word, count in words_count.most_common() if count == 1]
print('there {0} words only once to be removed'.format(len(once_words)))
print(most_words)
# print(once_words)
remove_words = set(most_words + once_words)
# print(remove_words)

inputs_new = [[word for word in text if word not in remove_words] for text in inputs_text]
new_all_counts = [word for text in inputs_new for word in text]
print('there new all context length is:{0}'.format(len(new_all_counts)))

# word2index and index2word processings
words_voca = set([word for text in inputs_new for word in text])
word2index = {}
index2word = {}
for i, word in enumerate(words_voca):
    word2index[word] = i
    index2word[i] = word
inputs_index = []
for text in inputs_new:
    inputs_index.append([word2index[word] for word in text])
print(len(inputs_index))
print(inputs_index[0][0:100])

model_glove = KeyedVectors.load_word2vec_format('glove.6B.300d.txt', binary=False)

n_features = 300
embeddings = np.random.uniform(-0.1, 0.1, (len(word2index), n_features))
inwords = 0
for word in words_voca:
    if word in model_glove.vocab:
        inwords += 1
        embeddings[word2index[word]] = model_glove[word]
print('there {} words in model_glove'.format(inwords))
print('The voca_word in presents text is:{0}'.format(len(words_voca)))
print('the precentage of words in glove is:{0}'.format(np.float(inwords) / len(words_voca)))

# truncate the sequence length
max_length = 1000
inputs_concat = []
for text in inputs_index:
    if len(text) > max_length:
        inputs_concat.append(text[0:max_length])
    else:
        inputs_concat.append(text + [0] * (max_length - len(text)))
print(len(inputs_concat))
inputs_index = inputs_concat
print(len(inputs_index))

# sampling the train data use category sampling
num_class = 8
label_unions = list(zip(inputs_index, labels_index))
print(len(label_unions))
trains = []
devs = []
tests = []
for c in range(num_class):
    type_sample = [union for union in label_unions if np.argmax(union[1]) == c]
    print('the length of this type length', len(type_sample), c)
    shuffle(type_sample)
    num_all = len(type_sample)
    num_train = int(num_all * 0.8)
    num_dev = int(num_all * 0.9)
    trains.extend(type_sample[0:num_train])
    devs.extend(type_sample[num_train:num_dev])
    tests.extend(type_sample[num_dev:num_all])
shuffle(trains)
shuffle(devs)
shuffle(tests)
print('the length of trains is:{0}'.format(len(trains)))
print('the length of devs is:{0}'.format(len(devs)))
print('the length of tests is:{0}'.format(len(tests)))

# --------------------------------------------------------------------
# ------------------------ model processing --------------------------
# --------------------------------------------------------------------
from ClassifierRNN import NN_config, CALC_config, ClassifierRNN

# parameters used by rnns
num_layers = 1
num_units = 60
num_seqs = 1000
step_length = 10
num_steps = int(num_seqs / step_length)
embedding_size = 300
num_classes = 8
n_words = len(words_voca)

# parameters used by trainning models
batch_size = 64
num_epoch = 100
learning_rate = 0.0075
show_every_epoch = 10

nn_config = NN_config(num_seqs=num_seqs, \
                      num_steps=num_steps, \
                      num_units=num_units, \
                      num_classes=num_classes, \
                      num_layers=num_layers, \
                      vocab_size=n_words, \
                      embedding_size=embedding_size, \
                      use_embeddings=False, \
                      embedding_init=embeddings)
calc_config = CALC_config(batch_size=batch_size, \
                          num_epoches=num_epoch, \
                          learning_rate=learning_rate, \
                          show_every_steps=10, \
                          save_every_steps=100)

print("this is checking of nn_config:\\\n",
      "out of num_seqs:{}\n".format(nn_config.num_seqs),
      "out of num_steps:{}\n".format(nn_config.num_steps),
      "out of num_units:{}\n".format(nn_config.num_units),
      "out of num_classes:{}\n".format(nn_config.num_classes),
      "out of num_layers:{}\n".format(nn_config.num_layers),
      "out of vocab_size:{}\n".format(nn_config.vocab_size),
      "out of embedding_size:{}\n".format(nn_config.embedding_size),
      "out of use_embeddings:{}\n".format(nn_config.use_embeddings))
print("this is checing of calc_config: \\\n",
      "out of batch_size {} \n".format(calc_config.batch_size),
      "out of num_epoches {} \n".format(calc_config.num_epoches),
      "out of learning_rate {} \n".format(calc_config.learning_rate),
      "out of keep_prob {} \n".format(calc_config.keep_prob),
      "out of show_every_steps {} \n".format(calc_config.show_every_steps),
      "out of save_every_steps {} \n".format(calc_config.save_every_steps))

rnn_model = ClassifierRNN(nn_config, calc_config)
rnn_model.fit(trains, restart=False)
accuracy = rnn_model.predict_accuracy(devs, test=False)
print("Final accuracy of devs is {}".format(accuracy))
test_accuracy = rnn_model.predict_accuracy(tests, test=False)
print("The final accuracy of tests is :{}".format(test_accuracy))