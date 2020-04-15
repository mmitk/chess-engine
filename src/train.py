import util
import alphabeta as ab 
import mcts
from env import chessGame
import chess 
from multiprocessing import Pool, Manager, Process
from models import model as md
from pathlib import Path

if __name__ == '__main__':
    model = md.svm()
    try:
        model.load_file(Path(util.HISTORY_DIR / 'alph_mct_1_model.pkl'))
    except Exception:
        print('oops')
    manager = Manager()
    a1 = ab.alphabeta_agent()
    m = mcts.mcts_agent(manager = manager, model = model)
    a2 = ab.alphabeta_agent(model = model)
    board = chess.Board()
    

    game = chessGame(a2, m)

    game.set_board(board)
    game.play_out()
    model.write_model(Path(util.HISTORY_DIR / 'alph_mct_1_model.pkl'))

