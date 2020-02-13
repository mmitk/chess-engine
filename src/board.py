import chess
import chess.svg

from IPython.display import SVG

class chessboard():
    def __init__(self):
        self.board = chess.Board()
        SVG(chess.svg.board(board=board,size=400)) 

    def get_board(self):
        return self.board 
