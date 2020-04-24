import chess.polyglot
import random
import numpy as np
import pandas as pd
import json
from models import model as md
import csv
from pathlib import Path
import util
import eval


class mishagent:
    
    def __init__(self, historic = False, filename=None, model = None):
        self.type = 1
        self.data = list()
        if not model is None:
            self.model = model
        else:
            self.model = md.svm(filename = filename, historic = historic)
        self.data = list()


    def make_move(self, depth, board):
        if board.is_checkmate():
            return None
        actions = {}
        for move in board.legal_moves:
            theta = self.predict_probability(board, move) 
            board.push(move)
            actions[move] = theta * self.quiesce(-100000, 100000, board)
            board.pop()

        best_move = max(actions, key=actions.get)
        self.data.append({'state': board.fen(),'move':best_move})
        print('.',end = '')
        return best_move
    
    def quiesce( self, alpha, beta, board ):
    # need to import evaluate.py
        stand_pat = eval.evaluate_board(board)
        if( stand_pat >= beta ):
            return beta
        if( alpha < stand_pat ):
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -self.quiesce( -beta, -alpha, board)
                board.pop()

                if( score >= beta ):
                    return beta
                if( score > alpha ):
                    alpha = score  
        return alpha

    def predict_probability(self, board, move):
        data = [{'state':board.fen(),'move':move}]
        #print('predicting for move: ', move)
        prec = md.preprocessor()
        prec.fit(raw_data = data)
        data = prec.transform(predict = True)
        return self.model.predict_proba(data)

    def write_data(self, filename, did_win = None):
        for row in self.data:
            if did_win == 1:
                row['didWin'] = did_win
            else:
                row['didWin'] = 0
        p = Path(util.HISTORY_DIR / 'history.csv')

        #df = pd.DataFrame()
        f = open(p, 'a')

        fieldnames = self.data[0].keys()

        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
        #csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
        for row in self.data:
            csvwriter.writerow(row)
        f.close()
     