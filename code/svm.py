from gensim.models.doc2vec import Doc2Vec
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report,confusion_matrix
import sys
import csv
import pickle

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
    mlp = svm.SVC()
    mlp.fit(X_train,y_train)
    model_file = open('svm.pkl', 'wb')
    pickle.dump(mlp, model_file)
    predictions = mlp.predict(X_test)
    print(confusion_matrix(y_test,predictions))
    print(classification_report(y_test,predictions))

if __name__ == "__main__":
    main()
