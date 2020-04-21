import chess 
import pandas as pd 
import numpy as np 
from models import model as md
import json
import multiprocessing
from multiprocessing import Pool, Manager
import os, sys
import datetime
import time 
import csv
from pathlib import Path
import random

import eval
import util
class mcts_agent(object):

    

    def __init__(self, manager, historic=False, filename = None, model = None):
        super().__init__
        self.type = 2

        #if historic == True and filename is not None:
            #self.model = md.svm_eval(filename = filename, historic )
        if not model is None:
            self.model = model
        else:
            self.model = md.svm(filename = filename, historic = historic)
        
        



    def play_value(self, board, depth = 5):
        if board.is_checkmate() or depth == 0:
            return -eval.evaluate_board(board)
    
        move = random.choice(board.legal_moves)
        theta = self.predict_probability(board, move)
        board.push(move)
        val = theta*(- self.play_value(board))
        board.pop()

        return val
       

    #def heuristic_value(self, board, move):
     #   theta = self.predict_probability(board, move)
     #   return theta * eval.evaluate_board(board), theta
       

    def monte_carlo_value(self, board, N = 5):
        scores = [self.play_value(board) for i in range(0, N)]
        return np.mean(scores)

    def make_move(self, board, depth = 50, player = 1):
        actions = {}
        if board.is_checkmate():
            return None
        for move in board.legal_moves:
            theta = self.predict_probability(board, move)
            if theta >= 0.5:
                board.push(move)
                actions[move] = theta *  (-self.monte_carlo_value(board))
                board.pop()

        
        v = max(actions, key=actions.get)

        self.data.append({'state': board.fen(),'move':v})
        return v

    def write_model(self, filename):
        self.model.write_file(util.MODELS_DIR / filename)

    def write_data(self, filename, did_win = None):
        dictlist = list(self.data)
        for row in dictlist:
            if did_win == 1:
                row['didWin'] = did_win
            else:
                row['didWin'] = 0
        p = Path(util.HISTORY_DIR / 'history.csv')
        f = open(p, 'a')

        fieldnames = dictlist[0].keys()

        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
        #csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
        for row in dictlist:
            csvwriter.writerow(row)
        f.close()

    def predict_probability(self, board, move):
        data = [{'state':board.fen(),'move':move}]
        #print('predicting for move: ', move)
        prec = md.preprocessor()
        prec.fit(raw_data = data)
        data = prec.transform(predict = True)
        return self.model.predict_proba(data)

    def log(self, message, msg_type=2):
        util.log(message, logger_str="mcts", msg_type=msg_type, write_to_console=False)
