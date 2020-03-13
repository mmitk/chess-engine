import chess 
import pandas as pd 
import numpy as np 
from models import model as md 
import json
import multiprocessing
from multiprocessing import Pool, Manager
import os
import datetime
import time 
import csv

import eval

class mcts_agent(object):
    def __init__(self, manager, historic=False, filename = None):
        super().__init__
        self.visits = manager.dict()
        self.differential = manager.dict()
        self.data = manager.list()
        #if historic == True and filename is not None:
            #self.model = md.svm_eval(filename = filename, historic )
        self.model = md.svm_eval(filename = filename, historic = historic)
        
    def record(self, board, score):
        self.visits["total"] = self.visits.get("total",1) + 1
        self.visits[board.fen()] =  self.visits.get(board.fen(), 0) + 1
        dataset = {'input': np.asarray(list(board.fen().encode('utf8'))), 'target': score}
        #self.data.append(dataset)
        self.log('Visit Recorded')
        return self.model.fit(dataset = self.data)

    def play_value(self, board, depth = 150):
        if board.is_checkmate() or depth == 0:
            self.record(board, eval.evaluate_board(board))
            return eval.evaluate_board(board)
    
        heuristic_vals = {}
        for move in board.pseudo_legal_moves:
            board.push(move)
            heuristic_vals[move] = self.heuristic_value(board)
            board.pop()
        move = max(heuristic_vals, key = heuristic_vals.get)

        board.push(move)
        value = -self.play_value(board, depth=depth-1)
        board.pop()
        self.record(board, value)
        #self.log('Playout Complete')
        return value

    def heuristic_value(self, board):
        dataset = [{'input': board.fen(), 'target': None}]
        self.data.append({'input':board.fen().encode('utf8'),  'target':eval.evaluate_board(board)})
        val = self.model.predict(dataset = board.fen(), formatted = False)
    #print(val)
        return np.mean(val)

    def monte_carlo_value(self, board, playouts = 50, N = 5):
        with Pool() as p:
            try:
                scores = p.map(self.play_value,[board.mirror() for i in range(0, playouts)])
            except Exception as e:
                return float('-inf')
        return np.mean(scores)

    def make_move(self, board, playouts = 100):
        actions = {}
        for move in board.pseudo_legal_moves:
            board.push(move)
            actions[move] = -self.monte_carlo_value(board)
            board.pop()
        self.log('move chosen')
        return max(actions, key = actions.get)

    def write_model(self, filename):
        self.model.write_file(filename)

    def write_data(self, filename):
        #input_data = {}
        #target_data = {}
        #i = 0
        #for row in list(self.data):
            #input_data[i] = row['input']
            #target_data[i] = row['target']
            #i+=1
        #input_df = pd.DataFrame.from_dict(input_data, orient='index')
            #print(input_df.head())
        #output_df = pd.DataFrame.from_dict(target_data, orient='index')
            #print(output_df.head())
        #df = pd.concat([input_df,output_df],axis = 1)
        #df.to_json(filename)
        dictlist = list(self.data)
        f = open('history.csv', 'w')

        fieldnames = dictlist[0].keys()

        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
        csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
        for row in dictlist:
            csvwriter.writerow(row)
        f.close()
        #with open(filename, 'a') as f:
            #json.dump(list(self.data), f)
            #f.write(os.linesep)
    
    def log(self, message):
        filename = '..\\logs\\'+str(datetime.date.today()) + '.log'
        try:
            with open(filename, 'a') as f:
                f.write(message + '\t'+str(time.ctime()))
                f.write(os.linesep)
        except Exception:
            with open(filename, 'w+') as f:
                f.write(message + '\t\t'+str(time.ctime()))
                f.write(os.linesep)
 
        
