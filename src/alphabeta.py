import chess.polyglot
import random
import numpy as np
from models import model as md
import pandas as pd
import json
from models import model as md
import eval
import csv
from pathlib import Path
import util


class alphabeta_agent:

    def __init__(self, historic = False, filename=None):
        self.data = list()
        self.model = md.svm(filename = filename, historic = historic)
        self.data = list()

    
    def alphabeta( self, alpha, beta, depthleft, board ):
        bestscore = -9999
        if( depthleft == 0 ):
            return self.quiesce( alpha, beta, board )
        for move in board.legal_moves:
            board.push(move)   
            score = -self.alphabeta( -beta, -alpha, depthleft - 1, board)
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

    def make_move(self, depth, board):
        if board.is_checkmate():
            return None
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            theta = self.predict_probability(board, move)
            if theta >= 0.3:
                board.push(move)
                boardValue = - self.alphabeta(-beta, -alpha, depth-1,board)
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
        prec = md.preprocessor()
        prec.fit(raw_data = data)
        data = prec.transform()
        return self.model.predict_proba(data)

    def write_data(self, filename, did_win = None):
        if did_win is not None:
            for row in self.__delattr__data:
                row['didWin'] = did_win
        p = Path(util.HISTORY_DIR / 'history.csv')
        f = open(p, 'a')

        #fieldnames = dictlist[0].keys()

        csvwriter = csv.DictWriter(f, delimiter=',')
        #csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
        for row in self.data:
            csvwriter.writerow(row)
        f.close()

  