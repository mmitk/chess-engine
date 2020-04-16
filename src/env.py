import chess 
from enum import IntEnum


class Winner(IntEnum):
    WHITE = 0
    BLACK = 1
    DRAW = 2


class chessGame:

    """
    The environment in which a game is played between two agents 
    """

    def __init__(self, agent1 = None, agent2 = None, model = None):
        self.board = chess.Board()
        self.winner = None 
        self.agent1 = agent1
        self.agent2 = agent2
        self.move_history = list()
        self.model = model


    def set_board(self, board, agent1 = None, agent2 = None):
        """
        update the game with a new board state
        """
        
        if not isinstance(board, str):
            self.board = board
        else:
            self.board = chess.Board(board)
        #else:
            #raise TypeError('parameter board in set_baord (env.py) must be of type str or chess.Board()')

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
        i = 0
        move_count = 0
        while not self.board.is_checkmate():
            move1 = self.agent1.make_move(depth = 3, board = self.board)
            if not move1 is None:
                 self.board.push(move1)
                 self.move_history.append({'state': self.board.fen(),'move1':move1})
            else:
                break
            
            # Now agent 2 selects and makes their move
            move2 = self.agent2.make_move(depth = 3, board = self.board)
            if not move2 is None:
                self.board.push(move2)
                self.move_history.append({'state': self.board.fen(),'move2':move2})
            else:
                break
            i+=1
            move_count += 1
            if (i >10):
                i = 0
                print('\n')
            

            
        

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
            print('Agent 1 Won!')
            self.agent1.write_data('moves_history.csv', 1)
            self.agent2.write_data('moves_history.csv', didWin = int(0))
        elif self.winner == Winner.BLACK:
            print('Agent 2 Won!')
            self.agent1.write_data('moves_history.csv', didWin = int(0))
            self.agent2.write_data('moves_history.csv', 1)

        for move in self.move_history:
            print(move)
    


    
