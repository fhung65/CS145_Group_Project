import numpy as np
import gensim
import csv

from time import gmtime, strftime
import logging
logtime = strftime("%Y-%m-%d_%H:%M:%S", gmtime())

logging.basicConfig(filename='logs/doc2vec_{}'.format(logtime), format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from test_tweets import *

#text = open('tweets.csv')
text = open('tweets4_preprocessed.csv')

corpus = []
for i, line in enumerate(csv.reader(text)):
    corpus.append(gensim.models.doc2vec.TaggedDocument(
                    #gensim.utils.simple_preprocess(line[0]),
                    line[0].split(),
                    [i]))

text.close()
sentences = [x.words for x in corpus]

model = gensim.models.doc2vec.Doc2Vec(size=100, window=5, min_count=2, iter=50)

model.build_vocab(corpus)

model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)

model.save('models/doc2vec_{}'.format(logtime))


#creating document vectors
happy_new_year = model.infer_vector(['happy', 'new', 'year'])

vs = [model.infer_vector(x) for x in test_tweets]

def test_dist(v1, v2):
    return np.linalg.norm(v1 - v2)

def test_all(l):
    ret = []
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            ret.append(
                    (test_dist(l[i], l[j]), i, j))
    return ret

# to verify vocab:
model.wv.most_similar(positive=['god'])

