import board
import search

movehistory =[]

board = board.chessboard()
chessboard = board.get_board()
mov = selectmove(3)
chessboard.push(mov)
SVG(chess.svg.board(board=board,size=400))