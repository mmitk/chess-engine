import chess 
import pandas as pd 
import numpy as np 
from models import model as md 
import json
import multiprocessing
from multiprocessing import Pool, Manager


import eval

class mcts_agent(object):
    def __init__(self, manager, historic=False):
        super().__init__
        self.visits = manager.dict()
        self.differential = manager.dict()
        self.data = manager.list()
        self.model = md.svm_eval()
        
    def record(self, board, score):
        self.visits["total"] = self.visits.get("total",1) + 1
        self.visits[board.fen()] =  self.visits.get(board.fen(), 0) + 1
        dataset = {'input': np.asarray(list(board.fen().encode('utf8'))), 'target': score}
        self.data.append(dataset)
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

        return value

    def heuristic_value(self, board):
        dataset = [{'input': board.fen(), 'target': None}]
        val = self.model.predict(dataset = board.fen(), formatted = False)
    #print(val)
        return np.mean(val)

    def monte_carlo_value(self, board, playouts = 100, N = 5):
        with Pool() as p:
            scores = p.map(self.play_value,[board.mirror() for i in range(0, playouts)])
        return np.mean(scores)

    def make_move(self, board, playouts = 100):
        actions = {}
        for move in board.pseudo_legal_moves:
            board.push(move)
            actions[move] = -self.monte_carlo_value(board)
            board.pop()
        return max(actions, key = actions.get)
 
    
 
        
