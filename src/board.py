import chess
import chess.svg

from IPython.display import SVG

class chessboard():
    def __init__(self):
        self.board = chess.Board()
 

    def get_board(self):
        return self.board 
    
    def svg(self):
        SVG(chess.svg.board(board=board,size=400))