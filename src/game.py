import board
import search

movehistory =[]

board = board.chessboard()
chessboard = board.get_board()
mov = search.selectmove(3,chessboard,movehistory)
chessboard.push(mov)
board.svg()