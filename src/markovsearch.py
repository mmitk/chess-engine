import chess.polyglot
import chess
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
    def __init__(self, historic = False, filename=None, model = None, utilities_file = None):
        self.type = 4
        self.data = list()
        if not model is None:
            self.model = model
        else:
            self.model = md.svm(filename = filename, historic = historic)
        self.data = list()
        if utilities_file is None:
            self.utilities = dict()
            print('no utility file')
        else:
            with open(utilities_file, 'r') as f:
                self.utilities = json.load(f)

    
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
        #stand_pat = eval.evaluate_board(board)
        try:
            stand_pat = self.utilities[board.fen()]
        except Exception:
            print('@',end='')
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

    def make_move(self, board, depth = None):
        if board.is_checkmate():
            print('.',end = '')
            return None
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            theta = self.predict_probability(board, move)
            board.push(move)
            boardValue = theta*(- self.alphabeta(-beta, -alpha, 0,board))
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


    def value_iteration(self,history_file, gamma = 0.7, num_iter = 100):
        history = pd.read_csv(history_file)
        history = history.drop_duplicates()
        history_dict = history.to_dict('records')

        U = dict()
        U_prime = dict()
        rewards = dict()
        states = list()
        # get reward for each given state and action
        # initialize u prime
        # each row in history_ is a row from the historic data 
        for row in history_dict:
            state = row['state']
            action = row['move']
            reward = float(row['class'])
            if reward == float(0.0):
                reward = float(-1)
            states.append(state)
            U[state] = eval.evaluate_board(chess.Board(state))/10
            #U_prime[state] = evaluate_board(chess.Board(state))
            if (state, action) in rewards.keys():
                count = rewards[(state, action)][1]
                curr_mean= rewards[(state, action)][0] 
                new_mean = ((count*curr_mean)+reward)/(count+1)
                rewards[(state, action)][0] = new_mean
                rewards[(state, action)][1] += 1
            else:
                rewards[(state, action)] = [0.0,0.0]
                rewards[(state, action)][0] = reward
                rewards[(state, action)][1] = 1
        
            
        for i in range(num_iter):
            for s in states:
                #Q = dict()
                max_Q = float("-inf")
                board = chess.Board(s)
                for a in board.legal_moves:
                    board.push(a)
                    if (s,a) in rewards.keys():
                        R = rewards[(s,a)][0]
                    else:
                        R = 0.0

                    s_prime = board.fen()
                    if s_prime in states:
                        V = U[s_prime]
                    else:
                        states.append(s_prime)
                        V = eval.evaluate_board(board)/10
                    Q = R + (gamma*V)
                    if Q > max_Q:
                        max_Q = Q

                    board.pop()

            if max_Q == float("-inf"):
                max_Q = eval.evaluate_board(chess.Board(s))/10
            U[s] = max_Q
            print('.',end='')
            self.utilities = U
            with open(Path(util.HISTORY_DIR / 'updated_utility.json'), 'w') as f:
                json.dump(U, f)
        #U_prime = pd.Series(U, name = 'utility')
        #U_prime.index.name='state'
        #U_p = pd.DataFrame(U_prime)
        #return U_prime,U
        self.utilities = U
        with open(Path(util.HISTORY_DIR / 'updated_utility.json'), 'w') as f:
            json.dump(U, f)



            
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
     
