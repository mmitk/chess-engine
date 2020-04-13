#import board
import search
import chess 
import chess.engine
import mcts
from multiprocessing import Pool, Manager, Process
import time
from datetime import date
import os.path
import util

if __name__ == '__main__':
    util.parse_cmd_line()
    movehistory1 = []
    movehistory2 = []
    util.init_data_dirs()
    board = chess.Board()
#chessboard = board.get_board()
    manager = Manager()
    manager2 = Manager()
    m1 = mcts.mcts_agent(manager)
    m2 = mcts.mcts_agent(manager2)


    while not board.is_checkmate():
        #move = m1.make_move(board)
        move = search.selectmove(3,board,movehistory1)
        print('Agent A plays: {}'.format(str(move)))
        board.push(move)

        #move = search.selectmove(3,board,movehistory1)
        move = m2.make_move(board, player = -1)
        board.push(move)
        print('Agent B plays: {}'.format(str(move)))

        #m.write_data('history.csv')
 


    print('History of Agent 1 (MCTS): ',movehistory1)


