from sklearn import svm
import pandas as pd
import pickle

class svm:
    
    def __init__(self, filename = None, historic = False):
        if historic and filename is not None:
            self._model = pickle.load(filename)
        else:
            if filename is not None:
                self._model = svm.SVC(kernel = 'rbf')
            else:
                df = pd.read_json(filename)
                target = df.pop('target')
                self._model=svm.SVC(kernel = 'rbf').fit(df, target)

    
    def fit(self, dataset, formatted = False):
        if not formatted:
            target = dataset.pop('target')
            self._model.fit(dataset, target)
    
    def predict(self, dataset, formatted = False):
        if not formatted:
            target = dataset.pop('target')
            return self._model.predict(dataset)

    def predict_proba(self, dataset, formatted = False):
         if not formatted:
            target = dataset.pop('target')
            return self._model.predict_proba(dataset)
    
    def write_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self._model, file)
    
    def load_file(self, filename):
        with open(filename, 'rb') as file:
            self._model = pickle.load(file)

