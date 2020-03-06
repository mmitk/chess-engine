from sklearn import svm
import pickle

class svm:
    
    def __init__(self, filename = None):
        if not filename:
            self._model = svm.SVC(kernel = 'rbf')
    
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
