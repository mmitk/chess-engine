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
    m = mcts.mcts_agent(manager)


    while not board.is_checkmate():
        move = search.selectmove(3,board,movehistory1)
        print('Agent A plays: {}'.format(str(move)))
        #move = search.make_move(board)
        #move = search.make_move(chessboard)
        board.push(move)
        #move = search.selectmove(3,board,movehistory2)
        #p = Process(target=m.make_move,args=(board,))
        move = m.make_move(board)
        #move = p.start()
        board.push(move)
        print('Agent B plays: {}'.format(str(move)))
#        m.write_model(util.MODELS_DIR / 'svm_eval.pkl')
        m.write_data('history.csv')
 
        #d = date.today()
        #t = time.ctime(time.time())
        #save_path = 'C:\\Users\\mmitk\\Documents\\School\\2020\\AI\\project\\backups'
        #backup = 'model_'+t + '.pkl'
        #m.write_model(backup.replace(" ", "").replace(".","-"))
        #completeName = os.path.join(save_path, backup)
        #m.write_model(completeName.replace(" ", "").replace(".","-"))
#board.svg()
    #m.write_model('svm_eval.pkl')
 
    #d = date.today()
    #backup = 'svm_eval' + d.isoformat() + '.pkl'

    print('History of Agent 1 (MCTS): ',movehistory1)


