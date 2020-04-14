from sklearn import svm as sv
import pandas as pd
import pickle
import chess
import numpy as np
#from __future__ import with_statement
import eval
import datetime
import time
import os
import util
class svm():
    
    def __init__(self, filename = None, historic = False, gam = 1/8):
        if filename is None:
                self._model = sv.SVC(kernel = 'rbf', gamma=gam, probability = True)


        elif filename is not None and historic == True:
            #self._model = svm.SVR(kernel = 'rbf')
            try:
                with open(filename, 'rb') as file:
                    self._model = pickle.load(file)
            except EnvironmentError as e:
                print(e)
                
                
        # placeholder!!!
        else: 
            self._model = sv.SVC(kernel = 'rbf', gamma=gam)
      
    
    def fit(self, dataset, formatted = True):
        y = dataset.pop('class')
        self._model.fit(dataset,y)
    
    def predict(self, dataset):
        try:
            self.model.predict
        except Exception as e:
            return False


    def predict_proba(self, dataset, formatted = True):
        try:
             self._model.predict_proba(dataset)[self._model.classes_.index(1)]
        except Exception:
            return 1
    
    def write_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self._model, file)
    
    def load_file(self, filename):
        with open(filename, 'rb') as file:
            self._model = pickle.load(file)


    def log(self, message):
        util.log(message,logger_str="svm_eval", debug_level=1)





class preprocessor(object):

    def __init__(self):
        super().__init__

    def fit(self, filename = None, raw_data = None):
        if filename is not None:
            self.raw_data = pd.read_csv(filename)
        elif raw_data is not None:
            self.raw_data = pd.DataFrame(raw_data)
        return self.raw_data

    def transform(self):
        data = self.raw_data
        data['state'] = data['state'].apply(self.serialize2)
        data = pd.concat([data['state'].apply(pd.Series), data['move']], axis = 1)
        data = data.rename(columns = {0:'b1',1:'b2',2:'b3',3:'b4',4:'b5'})
        data['b1'] = data['b1'].apply(np.log)
        data['b2'] = data['b2'].apply(np.log)
        data['b3'] = data['b3'].apply(np.log)
        data['b4'] = data['b4'].apply(np.log)
        move = data.pop('move')
        data = pd.concat([data,move.apply(self.listify).apply(pd.Series)], axis = 1)
        data = data.rename(columns = {0:'m1',1:'m2',2:'m3',3:'m4',4:'m5'})
        if not 'm5' in data.columns:
            data['m5'] = 0
        data['m1'] = data['m1'].apply(self.encode_move)
        data['m2'] = data['m2'].apply(self.encode_move)
        data['m3'] = data['m3'].apply(self.encode_move)
        data['m4'] = data['m4'].apply(self.encode_move)
        data['m5'] = data['m5'].apply(self.encode_move)
        return data
    
    def encode_move(self,m):
        try:
            val = ord(m)
            return val
        except Exception:
            if not isinstance(m, int):
                raise TypeError('Encoded Move must be of type str or int')
            else:
                return int(m)



    def listify(self,string):
        return list(str(string))
        
    def bin_matrix_to_decimal(self, matrix):
        m = matrix.reshape(-1)
        dec = 0
        j = len(m)-1
        for i in range(len(m)-1):
            if m[i]:
                dec += 2**j
            j -= 1
        return float(dec)

    def serialize(self,board):
        import numpy as np
        assert board.is_valid()

        bstate = np.zeros(64, np.uint8)
        for i in range(64):
            pp = board.piece_at(i)
            if pp is not None:
                #print(i, pp.symbol())
                bstate[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6, \
                        "p": 9, "n":10, "b":11, "r":12, "q":13, "k": 14}[pp.symbol()]
        if board.has_queenside_castling_rights(chess.WHITE):
            assert bstate[0] == 4
            bstate[0] = 7
        if board.has_kingside_castling_rights(chess.WHITE):
            assert bstate[7] == 4
            bstate[7] = 7
        if board.has_queenside_castling_rights(chess.BLACK):
            assert bstate[56] == 8+4
            bstate[56] = 8+7
        if board.has_kingside_castling_rights(chess.BLACK):
            assert bstate[63] == 8+4
            bstate[63] = 8+7

        if board.ep_square is not None:
            assert bstate[self.board.ep_square] == 0
            bstate[self.board.ep_square] = 8
        bstate = bstate.reshape(8,8)


        state = []
   
        state.append(self.bin_matrix_to_decimal((bstate>>3)&1))
        state.append(self.bin_matrix_to_decimal((bstate>>2)&1))
        state.append(self.bin_matrix_to_decimal((bstate>>1)&1))
        state.append(self.bin_matrix_to_decimal((bstate>>0)&1))

        state.append(((board.turn*1.0)+50))
    
        return state

    def serialize2(self,board):
        return self.serialize(chess.Board(str(board)))


    
    
        