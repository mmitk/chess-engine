import chess 
import enum


class Winner(IntEnum):
    WHITE = 0
    BLACK = 1
    DRAW = 2


class chessGame:

    """
    The environment in which a game is played between two agents 
    """

    def __init__(self, agent1 = None, agent2 = None):
        self.board = chess.Board()
        self.winner = None 
        self.agent1 = agent1
        self.agent2 = agent2


    def set_board(self, board, agent1 = None, agent2 = None):
        """
        update the game with a new board state
        """
        if isinstance(board, chess.Board()):
            self.board = board
        elif isinstance(board, str):
            self.board = chess.Board(board)
        else:
            raise TypeError('parameter board in set_baord (env.py) must be of type str or chess.Board()')

        if agent1 is not None:
            self.agent1 = agent1
        if agent2 is not None:
            self.agent2 = agent2

    def reset(self, agent1 = None, agent2 = None):
        """
        restart the game from scratch
        """
        self.board = chess.Board()
        self.winner = None 
        if agent1 is not None:
            self.agent1 = agent1
        if agent1 is not None:
            self.agent2 = agent2


    def play_out(self):
        """
        Playout the actual game between the two agents if they exist, otherwise raise an error
        Game loop iterates until a checkmate occurs
        """
        if self.agent1 is None or self.agent2 is None:
            raise ValueError('ERROR agent1 and agent2 can not be None for chessGame.play_out()')

        while not self.board.is_checkmate():
            move1 = self.agent1.make_move(board)
            self.board.push(move1)
            
            # Now agent 2 selects and makes their move
            move2 = self.agent2.make_move(board)
            self.board.push(move2)
        

        #set the Winner or if their is a draw
        if self.winner is None:
            result = self.board.result(claim_draw = True)
            if result == '1-0':
                self.winner = Winner.WHITE
            elif result == '0-1':
                self.winner = Winner.BLACK
            else:
                self.winner = Winner.DRAW

        # Now add to historic dataset of moves made by each agent
        if self.winner == Winner.WHITE:
            self.agent1.write_data('moves_history.csv', 1)
            self.agent2.write_data('moves_history.csv', 0)
        elif self.winner == Winner.BLACK:
            self.agent1.write_data('moves_history.csv', 0)
            self.agent2.write_data('moves_history.csv', 1)
    


    