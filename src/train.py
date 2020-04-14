import util
import alphabeta as ab 
import mcts
from env import chessGame
import chess 
from multiprocessing import Pool, Manager, Process

if __name__ == '__main__':
    util.parse_cmd_line()

    manager = Manager()
    a1 = ab.alphabeta_agent()
    m = mcts.mcts_agent(manager)
    a2 = ab.alphabeta_agent()
    board = chess.Board()

    game = chessGame(a1, a2)

    game.set_board(board)
    game.play_out()
