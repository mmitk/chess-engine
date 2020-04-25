import util
import time
import alphabeta as ab 
import mcts
import os
from env import chessGame
import chess 
import chess.engine
from multiprocessing import Pool, Manager, Process
from models import model as md
from pathlib import Path
import csv
import json

def update_total(time = None):
    with open(Path(util.HISTORY_DIR / 'stats.json'), 'r') as f:
        totals = json.load(f)

    total_time = int(totals['Total Session Time'])
    total_sessions = int(totals['Total Sessions'])
    total_sessions += 1
    totals['Total Sessions'] = total_sessions
    if not time is None:
        total_time += time
        totals['Total Session Time'] = total_time

    with open(Path(util.HISTORY_DIR / 'stats.json'), 'w') as f:
        json.dump(totals, f)
    


def session_0(model, num_iter = 30):
    start = time.time()
    util.log('STARTED: Session type 0 MonteCarlo and Alphabeta iterative Play', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    for i in range(num_iter):
        
        # new game is initaited with new agents and manager for 
        # pools

        manager = Manager()
        board = chess.Board()
        m = mcts.mcts_agent(manager = manager, model = model)
        a2 = ab.alphabeta_agent(model = model)

        if i%2 == 0:
            white = m
            black = a2 
        else:
            white = a2
            black = m 

        game = chessGame(white, black)
        game.set_board(board)

        #game plays out
        game.play_out()

    

        # model updates from history.csv, what was updated by both agents during gameplay
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
        game.reset()

    end = time.time()
            
    exec_time = (end - start)
    update_total(exec_time)
    message = 'COMPLETED: Session type 0 MonteCarlo and Alphabeta iterative Play\nExecution Time: {} seconds\n********************************************************'.format(exec_time)
    util.log(message, logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')


def session_1(model, num_iter = 30):
    util.log('Session type 1 started Stockfish and Alphabeta iterative Play', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    start = time.time()
    for i in range(num_iter):
        
        # new game is initaited with new agents and manager for 
        # pools

        board = chess.Board()
        a1 = ab.alphabeta_agent(model = model)
        a2 = stockfish_agent()

        if i%2 == 0:
            white = a1
            black = a2 
        else:
            white = a2
            black = a1 

         
        game = chessGame(white, black)
        game.set_board(board)

        #game plays out
        game.play_out()

    

        # model updates from history.csv, what was updated by both agents during gameplay
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
        game.reset()

    end = time.time()
            
    exec_time = (end - start)
    update_total(exec_time)
    message = 'COMPLETED Session type 1 Stockfish and Alphabeta iterative Play\nExecution Time: {} seconds\n********************************************************'.format(exec_time)
    util.log(message, logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')


def session_2(model):
    util.log('Session type 2 started Stockfish and Stockfish iterative Play', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    start = time.time()
    for i in range(20):
        
        # new game is initaited with new agents and manager for 
        # pools

        board = chess.Board()
        a1 = stockfish_agent()
        a2 = stockfish_agent()

         
        game = chessGame(a1, a2)
        game.set_board(board)

        #game plays out
        game.play_out()

    

        # model updates from history.csv, what was updated by both agents during gameplay
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
        game.reset()

    end = time.time()
            
    exec_time = (end - start)
    update_total(exec_time)
    message = 'COMPLETED Session 2 Stockfish and Stockfish iterative Play\nExecution Time: {} seconds\n********************************************************'.format(exec_time)
    util.log(message, logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')


def session_3(model, num_iter = 20):
    start = time.time()
    util.log('STARTED: Session type 3 MonteCarlo and MonteCarlo iterative Play', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    for i in range(num_iter):
        
        # new game is initaited with new agents and manager for 
        # pools

        manager = Manager()
        board = chess.Board()
        m = mcts.mcts_agent(manager = manager, model = model)
        m2 = mcts.mcts_agent(manager = manager, model = model)

        game = chessGame(m, m2)
        game.set_board(board)

        #game plays out
        game.play_out()

    

        # model updates from history.csv, what was updated by both agents during gameplay
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
        game.reset()

    end = time.time()
            
    exec_time = (end - start)
    update_total(exec_time)
    message = 'COMPLETED: Session type 0 MonteCarlo and MonteCarlo iterative Play\nExecution Time: {} seconds\n********************************************************'.format(exec_time)
    util.log(message, logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')

def session_4(model, num_iter = 50):
    start = time.time()
    util.log('STARTED: Session type 4 Stockfish and Stockfish iterative Play', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    for i in range(num_iter):
        
        # new game is initaited with new agents and manager for 
        # pools

        manager = Manager()
        board = chess.Board()
        s = stockfish_agent()
        s2 = stockfish_agent()

        game = chessGame(s, s2)
        game.set_board(board)

        #game plays out
        game.play_out()

    

        # model updates from history.csv, what was updated by both agents during gameplay
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
        game.reset()

    end = time.time()
            
    exec_time = (end - start)
    update_total(exec_time)
    message = 'COMPLETED: Session type 4 Stockfish and Stockfish iterative Play\nExecution Time: {} seconds\n********************************************************'.format(exec_time)
    util.log(message, logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')



class stockfish_agent:

    

    def __init__(self):
        self.type = 3
        ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
        path = Path(ROOT_DIR / 'stockfish-11-linux')
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish-11-linux/Linux/stockfish_20011801_x64")
        self.data = list()
    
    def make_move(self, board, depth = None):
        result = self.engine.play(board, chess.engine.Limit(time=0.3))
        self.data.append({'state': board.fen(),'move':result.move})
        return result.move

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


if __name__ == '__main__':
    model = md.svm()
    try:
        prec = md.preprocessor()
        prec.fit(filename = Path(util.HISTORY_DIR / 'history.csv'))
        data = prec.transform()
        model.fit(data)
        model.write_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
    except Exception:
        try:
            model.load_file(Path(util.HISTORY_DIR / 'test_model_1.pkl'))
        except Exception as e:
            print('oops: {}'.format(e))
    
    #a1 = ab.alphabeta_agent()
    
    
    session_4(model, 500)
    #session_1(model, 200)
    
 

