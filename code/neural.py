from gensim.models.doc2vec import Doc2Vec
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import scipy.stats

import pickle
import sys
import csv
from multiprocessing import Pool
import re
import numpy as np

layer_specs = [
    (30, 30),
    (30, 30, 30),
    (40, 40),
    (40, 40, 40),
    (50, 50),
    (50, 50, 50),
    (50, 50, 50, 50),
]

activations = [
    'logistic',
    'relu',
    'tanh',
]

def run_layers(layer_spec=(30,30,30)):
    spec_string = re.sub(' ', '_', str(layer_spec))
    logfile = open('logs/net_log_{}.txt'.format(spec_string), 'w')

    if (len(sys.argv) != 3):
        logfile.write("requires cleaned data csv and model filenames as arguments" +'\n')
        sys.exit(1)
    X = []
    y = []
    dataCSVFilename = sys.argv[1]
    modelFilename = sys.argv[2]
    model = Doc2Vec.load(modelFilename)
    with open(dataCSVFilename, 'r') as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            X.append(model.infer_vector(line[0].split()))
            y.append(1 if int(line[1]) > 0 else 0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    mlp = MLPClassifier(hidden_layer_sizes=layer_spec)
    mlp.fit(X_train,y_train)


    model_file = open('mlp_30_30_relu.pkl', 'wb')
    pickle.dump(mlp, model_file)

    predictions = mlp.predict(X_test)
    logfile.write(str(confusion_matrix(y_test,predictions)) +'\n')
    logfile.write(str(classification_report(y_test,predictions)) +'\n')
    logfile.close()


    return X_train, X_test, y_train, y_test, predictions


def run_activation(activation='identity'):
    layer_spec=(30,30,30)
    spec_string = 'spec_' + re.sub(' ', '_', str(layer_spec))
    logfile = open('logs/net_log_{}.txt'.format(spec_string+'_'+activation), 'w')

    if (len(sys.argv) != 3):
        logfile.write("requires cleaned data csv and model filenames as arguments" +'\n')
        sys.exit(1)
    X = []
    y = []
    dataCSVFilename = sys.argv[1]
    modelFilename = sys.argv[2]
    model = Doc2Vec.load(modelFilename)
    with open(dataCSVFilename, 'r') as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            X.append(model.infer_vector(line[0].split()))
            y.append(1 if int(line[1]) > 0 else 0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    mlp = MLPClassifier(hidden_layer_sizes=layer_spec, activation=activation)
    mlp.fit(X_train,y_train)
    predictions = mlp.predict(X_test)
    logfile.write(str(confusion_matrix(y_test,predictions)) +'\n')
    logfile.write(str(classification_report(y_test,predictions)) +'\n')
    logfile.close()

def load_data_and_mod(dataCSVFilename=''):

    if (len(sys.argv) != 3):
        logfile.write("requires cleaned data csv and model filenames as arguments" +'\n')
        sys.exit(1)
    X = []
    y = []

    if (dataCSVFilename == ''):
        dataCSVFilename = sys.argv[1]

    modelFilename = sys.argv[2]
    model = Doc2Vec.load(modelFilename)
    with open(dataCSVFilename, 'r') as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            X.append(model.infer_vector(line[0].split()))
            y.append(1 if int(line[1]) > 0 else 0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    model_file = open('mlp_30_30_relu.pkl', 'rb')
    mod = pickle.load(model_file)

    return X_train, X_test, y_train, y_test, mod

def thresh_test(prob, t):
    def thresh(p):
        if p < t:
            return 0
        else:
            return 1

    return np.vectorize(thresh)(prob[:,1])

def roc(data_mat, ground_truths, mod, thresholds):
    prob = mod.predict_proba(data_mat)
    l = []
    for t in thresholds:
        y = thresh_test(prob, t)
        conf_mat = confusion_matrix(ground_truths, y)
        tp = conf_mat[1,1]
        fp = conf_mat[0,1]
        tn = conf_mat[0,0]
        fn = conf_mat[1,0]


        l.append((1.0 - tn*1.0/(tn + fp), tp*1.0/(tp + fn)))
    return l

query_keys = [
'UCLA',
'bitcoin',
'christmas',
'coco',
'lafd',
'lapd',
'morning',
'reputation',
'terrycrews',
'thanksgiving',
'trump',
]

def queried_tweets_test(key):
    filename = 'queried_tweets/second_pass_preprocess/{}_second_pass.csv'.format(key)
    X_train, X_test, y_train, y_test, mod = load_data_and_mod(filename)

    data_list = X_train + X_test
    gt_list = y_train + y_test

    prob = mod.predict_proba(data_list)
    y = thresh_test(prob, 0.5)

    writer = csv.writer(open('{}_prediction.csv'.format(key), 'w'))

    for line in prob:
        writer.writerow(list(line))

    #plt.hist(prob, bins = 'auto')
    #plt.title(key)
    #plt.show()

def main():
    p = Pool(8)
    p.map(run_layers, layer_specs[:1])
    #p.map(run_activation, activations)

if __name__ == "__main__":
    #main()
    #res = run_layers(layer_specs[0])
    #X_train, X_test, y_train, y_test, mod = load_data_and_mod()
    #thresholds = np.arange(0, 1, 0.01)
    #pts = roc(X_test, y_test, mod, thresholds)

    for key in query_keys:
        queried_tweets_test(key)
