#import board
import search
import chess 
import chess.engine
import mcts
from multiprocessing import Pool, Manager, Process
import time
from datetime import date
import os.path

if __name__ == '__main__':
    movehistory1 = []
    movehistory2 = []

    board = chess.Board()
#chessboard = board.get_board()
    manager = Manager()
    m = mcts.mcts_agent(manager,historic = True, filename = 'svm_eval.pkl')


    while not board.is_checkmate():
        move = search.selectmove(3,board,movehistory1)
        print('move made Agent A')
        #move = search.make_move(board)
        #move = search.make_move(chessboard)
        board.push(move)
        #move = search.selectmove(3,board,movehistory2)
        #p = Process(target=m.make_move,args=(board,))
        move = m.make_move(board)
        #move = p.start()
        board.push(move)
        print('move made Agent B')
        m.write_model('svm_eval.pkl')
 
        d = date.today()
        t = time.ctime(time.time())
        save_path = 'C:\\Users\\mmitk\\Documents\\School\\2020\\AI\\project\\backups'
        backup = 'model_'+t + '.pkl'
        #m.write_model(backup.replace(" ", "").replace(".","-"))
        #completeName = os.path.join(save_path, backup)
        #m.write_model(completeName.replace(" ", "").replace(".","-"))
#board.svg()
    #m.write_model('svm_eval.pkl')
 
    #d = date.today()
    #backup = 'svm_eval' + d.isoformat() + '.pkl'

    print('History of Agent 1 (MCTS): ',movehistory1)


'''
if __name__ == "main":
    engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")

    board = chess.Board()
    while not board.is_game_over():
        resultEngine = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(resultEngine.move)


    engine.quit()
'''