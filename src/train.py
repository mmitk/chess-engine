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
        try:
             prec = md.preprocessor()
             prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
             data = prec.transform()
             model.fit(data)
             model.write_file(Path(util.HISTORY_DIR / 'alph_mct_1_model.pkl'))
        except Exception as e:
            print('oops: {}'.format(e))
    
    #a1 = ab.alphabeta_agent()
    
    

    

    for i in range(10):
        
        # new game is initaited with new agents and manager for 
        # pools

        #manager = Manager()
        board = chess.Board()
        a1 = ab.alphabeta_agent(model = model)
        #m = mcts.mcts_agent(manager = manager, model = model)
        a2 = ab.alphabeta_agent(model = model)

        game = chessGame(a2, a1)
        game.set_board(board)

        #game plays out
        game.play_out()

    

        # model updates from history.csv, what was updated by both agents during gameplay
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'alph_mct_1_model.pkl'))
        game.reset()
       
