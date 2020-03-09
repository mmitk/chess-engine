from sklearn import svm
import pandas as pd
import pickle
import chess
import numpy as np
import eval

class svm_eval():
    
    def __init__(self, filename = None, historic = False):
        if filename is None:
                self._model = svm.SVR(kernel = 'rbf')

        #placeholder!!!
        else:
            self._model = svm.SVR(kernel = 'rbf')
      
    
    def fit(self, dataset, formatted = True):
        if formatted and dataset is not None:
            df = pd.DataFrame(dataset)
            target = dataset.pop('target')
            self._model.fit(dataset, target)
            '''
        if formatted == False:
            df = pd.DataFrame(dataset)
            for i in range(df.input):
                df.input[i] = np.asarray(list(df.input[i].encode('utf8')))
            self._model.fit(df)
            '''

    
    def predict(self, dataset, formatted = True):
        if formatted==False and dataset is not None:
            #df = pd.DataFrame(dataset)
            #for inp in df.input:
                #inp = list(inp.encode('utf8'))
            try:
                return self._model.predict(np.asarray(list(dataset.encode('utf8'))).reshape(-1, 1))
            except Exception as e:
                #print('EVAL VALUE:',eval.evaluate_board(chess.Board(dataset.input[0].decode('utf8'))))
                df = pd.DataFrame(np.asarray(list(dataset.encode('utf8'))))
                df['target'] = float(eval.evaluate_board(chess.Board(dataset)))
                target = df.pop('target')
                self._model.fit(df, target)
                return self._model.predict(np.asarray(list(dataset.encode('utf8'))).reshape(-1, 1))

    def predict_proba(self, dataset, formatted = True):
         if formatted and dataset is not None:
            target = dataset.pop('target')
            return self._model.predict_proba(dataset)
    
    def write_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self._model, file)
    
    def load_file(self, filename):
        with open(filename, 'rb') as file:
            self._model = pickle.load(file)



'''
        #elif historic and filename is not None:
        #    self._model = pickle.load(filename)
        #elif filename is not None and not historic:
        #    df = pd.read_json(filename)
        #    target = df.pop('target')
        #    self._model=svm.SVC(kernel = 'rbf').fit(df, target)
'''