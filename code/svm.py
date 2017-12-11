from gensim.models.doc2vec import Doc2Vec
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report,confusion_matrix
import numpy as np
import sys
import csv
import pickle

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

def getData():
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
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.1)
    return X_test, y_test

def main():
    if (len(sys.argv) != 3):
        print("requires cleaned data csv and model filenames as arguments")
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
    mlp = svm.SVC(probability = True)
    mlp.fit(X_train,y_train)
    model_file = open('svm.pkl', 'wb')
    pickle.dump(mlp, model_file)
    predictions = mlp.predict(X_test)
    print(confusion_matrix(y_test,predictions))
    print(classification_report(y_test,predictions))

if __name__ == "__main__":
    main()
    # X_test, y_test = getData()
    # thresholds = np.arange(0, 1, 0.01)
    # pts = roc(X_test, y_test, pickle.load(open('svm.pkl', 'rb')), thresholds)
