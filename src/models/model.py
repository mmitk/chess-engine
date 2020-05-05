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
    
    def __init__(self, filename = None, historic = False, gam = 1/69, eval = False):
        if eval is True:
            #gam = 1/64
            self._model = sv.SVR(kernel = 'rbf')
            
        elif filename is None:
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
        dataset = dataset.drop_duplicates()
        y = dataset.pop('class')
        self._model.fit(dataset,y)
    
    def predict(self, dataset):
        try:
            return self._model.predict(dataset)
        except Exception as e:
            print(e)
            return False


    def predict_proba(self, dataset, formatted = True):
        try:
             return float(self._model.predict_proba(dataset)[:, np.where(self._model.classes_ == 1)].item(0))
        except Exception as e:
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

    def fit(self, filename = None, raw_data = None, dataframe = None):
        if filename is not None:
            self.raw_data = pd.read_csv(filename)
        elif raw_data is not None:
            self.raw_data = pd.DataFrame(raw_data)
        else:
            self.raw_data = dataframe
        return self.raw_data

    def transform(self, predict = False):
        data = self.raw_data
        if not predict:
            class_ = data.pop('class')
        data['state'] = data['state'].apply(self.serialize2)
        if not eval:
            data = pd.concat([data['state'].apply(pd.Series), data['move']], axis = 1)
            move = data.pop('move')
            move = move.apply(self.listify).apply(pd.Series)

        #data = pd.concat([data,move.apply(self.listify).apply(pd.Series)], axis = 1)
            move = pd.DataFrame(move).rename(columns = {0:'m1',1:'m2',2:'m3',3:'m4',4:'m5'})

            try:
                move['m5'] = move['m5'].apply(self.encode_move)
            except Exception:
                move['m5'] = 0

            move['m1'] = move['m1'].apply(self.encode_move)
            move['m2'] = move['m2'].apply(self.encode_move)
            move['m3'] = move['m3'].apply(self.encode_move)
            move['m4'] = move['m4'].apply(self.encode_move)

        
            data = pd.concat([data,move], axis = 1)
            if not predict:
                data = pd.concat([data,class_], axis = 1)
            return data
        
        else:
            if not predict:
                data = pd.concat([data['state'].apply(pd.Series), class_], axis = 1)
            else:
                data = data['state'].apply(pd.Series)
        return data
    
    def encode_move(self,m):
        try:
            val = ord(m)
            return val
        except Exception:
            return 0



    def listify(self,string):
        return list(str(string))
        
    def bin_matrix_to_decimal(self, state):
        new_state = list()
        ret_state = list()
        for i in range(0,8):
            for j in range(0,8):
                new_state.append((np.array([state[0][i][j],state[1][i][j],state[2][i][j],state[3][i][j]])))
        for i in range(64):
            ret_state.append(int(np.packbits(new_state[i])))
        return ret_state
            

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
            assert bstate[board.ep_square] == 0
            bstate[board.ep_square] = 8
        bstate = bstate.reshape(8,8)

        state = np.zeros((4,8,8), np.uint8)
        
        state[0] = (bstate>>3)&1
        state[1] = (bstate>>2)&1
        state[2] = (bstate>>1)&1
        state[3] = (bstate>>0)&1
        """
        state.append(self.bin_matrix_to_decimal((bstate>>3)&1))
        state.append(self.bin_matrix_to_decimal((bstate>>2)&1))
        state.append(self.bin_matrix_to_decimal((bstate>>1)&1))
        state.append(self.bin_matrix_to_decimal((bstate>>0)&1))
        """

        new_state = self.bin_matrix_to_decimal(state)
        new_state.append(board.turn*1.0)
    
        return new_state

    def serialize2(self,board):
        return self.serialize(chess.Board(str(board)))





    
    
        
