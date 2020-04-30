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


class markovagent:
    def __init__(self, historic = False, filename=None, model = None):
        self.type = 4
        self.data = list()
        if not model is None:
            self.model = model
        else:
            self.model = md.svm(filename = filename, historic = historic)
        self.data = list()

    
    def alphabeta( self, alpha, beta, depthleft, board ):
        bestscore = -9999
        if( depthleft == 0 ):
            return self.quiesce( alpha, beta, board )
        for move in board.legal_moves:
            #theta = self.predict_probability(board, move)
            board.push(move)   
            score = float(-self.alphabeta( -beta, -alpha, depthleft - 1, board))
            board.pop()
            if( score >= beta ):
                return score
            if( score > bestscore ):
                bestscore = score
            if( score > alpha ):
                alpha = score
        return bestscore

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

    def make_move(self, board, depth = 1):
        if board.is_checkmate():
            return None
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            theta = self.predict_probability(board, move)
            board.push(move)
            boardValue = theta*(- self.alphabeta(-beta, -alpha, depth-1,board))
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()
        self.data.append({'state': board.fen(),'move':bestMove})
        print('.',end = '')
        return bestMove

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
        p = Path(util.HISTORY_DIR / filename)

        #df = pd.DataFrame()
        f = open(p, 'a')

        fieldnames = self.data[0].keys()

        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
        #csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
        for row in self.data:
            csvwriter.writerow(row)
        f.close()
     