import board
import chess.polyglot
import random
import numpy as np
from models import svm
import pandas as pd
import eval

# UCT MCTS implemented here
###################################################################################################
visits = {}
differential = {}
data = []
model = svm
def record(board, score):
    visits["total"] = visits.get("total",1) + 1
    visits[board.fen()] =  visits.get(board.fen(), 0) + 1
    dataset = [{'input': board.fen(), 'target': score}]
    data.append(dataset)
    return model.fit(data)

def heuristic_value(board):
    dataset = [{'input': board.fen(), 'target': None}]
    return model.predict(pd.DataFrame(dataset))

def play_value(board, movehistory = None):
    if board.is_checkmate():
        record(board, eval.evaluate_board(board))
        return eval.evaluate_board(board)
    
    heuristic_vals = {}
    for move in board.legal_moves:
        board.push(move)
        heuristic_vals[move] = -heuristic_value(board)
        board.pop
    move = max(heuristic_vals, key = heuristic_vals.get)
    board.push(move)
    value = -play_value(board)
    board.pop()
    record(board, value)

    return value

def monte_carlo (board, N = 150):
    scores = [play_value(board) for i in range(0, N)]
    return np.mean(scores)

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