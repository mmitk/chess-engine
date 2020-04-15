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

import eval
import util
class mcts_agent(object):
    def __init__(self, manager, historic=False, filename = None, model = None):
        super().__init__
        self.visits = manager.dict()
        self.differential = manager.dict()
        self.data = manager.list()
        #if historic == True and filename is not None:
            #self.model = md.svm_eval(filename = filename, historic )
        if not model is None:
            self.model = model
        else:
            self.model = md.svm(filename = filename, historic = historic)
        
        
    def record(self, board, score):
        self.visits["total"] = self.visits.get("total",1) + 1
        self.visits[board.fen()] =  self.visits.get(board.fen(), 0) + 1
        #dataset = {'input': np.asarray(list(board.fen().encode('utf8'))), 'target': score}
        #self.data.append(dataset)
        self.log('Visit Recorded', msg_type=2)
        #return self.model.fit(dataset = self.data)
        return eval.evaluate_board(board)

    def play_value(self, board, depth = 5):
        if board.is_checkmate() or depth == 0:
            self.record(board, eval.evaluate_board(board))
            return eval.evaluate_board(board)
    
        heuristic_vals = {}
        for move in board.legal_moves:
            board.push(move)
            val = self.heuristic_value(board, move)
            if val is not None:
                heuristic_vals[move] = val[0]
            board.pop()
        move = max(heuristic_vals, key = heuristic_vals.get)
        board.push(move)
        value = self.play_value(board, depth=depth-1)
        #print("value" + str(value))
        board.pop()
        self.record(board, value)
        #self.log('Playout Complete')
        return value

    def heuristic_value(self, board, move):
        data = [{'state':board.fen(),'move':move}]
        prec = md.preprocessor()
        prec.fit(raw_data = data)
        data = prec.transform()
        theta = self.model.predict_proba(data)
        return theta * eval.evaluate_board(board), theta
       

    def monte_carlo_value(self, board, playouts = 15, N = 5):
        scores = []
        with Pool() as p:
            try:
                scores = p.map(self.play_value,[board.mirror() for i in range(0, playouts)])
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                util.log(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + ":" + str(e), logger_str="EXCEPTION", write_to_console=False)
                return(float('-inf'))
        return np.mean(scores)

    def make_move(self, board, depth = 50, player = 1):
        actions = {}
        predicted = {}
        if board.is_checkmate():
            return None
        for move in board.legal_moves:
            theta = self.heuristic_value(board,move)[1]
            if theta >= 0.5:
                board.push(move)
                actions[move] = player * self.monte_carlo_value(board)
                predicted[move] = theta
                board.pop()
        #for k, v in actions.items():
            #print(str(k) + " = " + str(v))
        
        v = max(actions, key=actions.get)
        #else:
            #v = min(actions, key=actions.get)
        self.data.append({'state': board.fen(),'move':v})
        return v

    def write_model(self, filename):
        self.model.write_file(util.MODELS_DIR / filename)

    def write_data(self, filename, didWin = None):
        dictlist = list(self.data)
        for row in dictlist:
            if didWin == 1:
                row['didWin'] = didWin
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
    def log(self, message, msg_type=2):
        util.log(message, logger_str="mcts", msg_type=msg_type, write_to_console=False)
