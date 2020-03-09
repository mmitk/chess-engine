import board
import search
import chess 
import chess.engine

movehistory =[]

board = board.chessboard()
chessboard = board.get_board()
#mov = search.selectmove(3,chessboard,movehistory)
move = search.make_move(chessboard)
chessboard.push(move)
board.svg()
'''
if __name__ == "main":
    engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")

    board = chess.Board()
    while not board.is_game_over():
        resultEngine = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(resultEngine.move)


    engine.quit()
'''