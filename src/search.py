import board
import chess.polyglot
import random
import numpy as np
from models import model as md
import pandas as pd
import json
import eval

# UCT MCTS implemented here
# currently uses handwritten board evauluation
# and SVM to calulate (predict) Heursitic values
###################################################################################################
visits = {}
differential = {}
data = []
#model = md.svm_eval()

# record new states and scores
# and retrain models based on these moves (states)
def record(board, score):
    print('record func')
    visits["total"] = visits.get("total",1) + 1
    visits[board.fen()] =  visits.get(board.fen(), 0) + 1
    dataset = [{'input': board.fen().encode('utf8'), 'target': score}]
    data.append(dataset)
    return model.fit(data)

# return a predicted (calculated) heuristic given a certain move
def heuristic_value(board):
    print('heuristic_value func')
    dataset = [{'input': board.fen(), 'target': None}]
    val = model.predict(dataset = board.fen(), formatted = False)
    #print(val)
    return val[0]

def play_value(board, movehistory = None):
    print('play_value')
    if board.is_checkmate():
        record(board, eval.evaluate_board(board))
        return eval.evaluate_board(board)
    
    heuristic_vals = {}
    for move in board.pseudo_legal_moves:
        board.push(move)
        heuristic_vals[move] = -heuristic_value(board)
        board.pop()
    move = max(heuristic_vals, key = heuristic_vals.get)

    board.push(move)
    value = -play_value(board)
    board.pop()
    record(board, value)
 
    return value

def monte_carlo (board, N = 150):
    print('monte_carlo func')
    scores = [play_value(board) for i in range(0, N)]
    return np.mean(scores)

def make_move(board):
    print('make_move func')
    actions = {}
    for move in board.pseudo_legal_moves:
        board.push(move)
        actions[move] = -monte_carlo(board)
        board.pop()
    return max(actions, key = actions.get)

def append_data(filename, data):
    with open(filename, 'a') as f:
        json.dump(data, f)
        f.write(os.linesep)

####################################################################################################

# classic alphabeta search with quiesce
####################################################################################################
# added board as a parameter, to be passed to in main
def alphabeta( alpha, beta, depthleft, board ):
    bestscore = -9999
    if( depthleft == 0 ):
        return quiesce( alpha, beta, board )
    for move in board.legal_moves:
        board.push(move)   
        score = -alphabeta( -beta, -alpha, depthleft - 1, board)
        board.pop()
        if( score >= beta ):
            return score
        if( score > bestscore ):
            bestscore = score
        if( score > alpha ):
            alpha = score
    return bestscore


def quiesce( alpha, beta, board ):
    # need to import evaluate.py
    stand_pat = eval.evaluate_board(board)
    if( stand_pat >= beta ):
        return beta
    if( alpha < stand_pat ):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce( -beta, -alpha, board)
            board.pop()

            if( score >= beta ):
                return beta
            if( score > alpha ):
                alpha = score  
    return alpha


def selectmove(depth, board, movehistory):
    try:
        move = chess.polyglot.MemoryMappedReader("bookfish.bin").weighted_choice(board).move()
        movehistory.append(move)
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth-1,board)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if( boardValue > alpha):
                alpha = boardValue
            board.pop()
        movehistory.append(bestMove)
        return bestMove