#import board
import search
import chess 
import chess.engine
import mcts
from multiprocessing import Pool, Manager, Process

if __name__ == '__main__':
    movehistory1 = []
    movehistory2 = []

    board = chess.Board()
#chessboard = board.get_board()
    manager = Manager()
    m = mcts.mcts_agent(manager,False)

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
#board.svg()
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