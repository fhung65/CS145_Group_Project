import numpy as np
import gensim
import csv

text = open('tweets.csv')

corpus = []
for i, line in enumerate(csv.reader(text)):
    corpus.append(gensim.models.doc2vec.TaggedDocument(
                    #gensim.utils.simple_preprocess(line[0]),
                    line[0],
                    [i]))

text.close()

model = gensim.models.doc2vec.Doc2Vec(size=50, min_count=2, iter=55)

model.build_vocab(corpus)

model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)

happy_new_year = model.infer_vector(['happy', 'new', 'year'])
