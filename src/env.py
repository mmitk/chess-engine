import chess 
from enum import IntEnum
from pathlib import Path
import util
import time
import json
import datetime


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
        self.move_history = list()


    def play_out(self, depth = 1, stats_file = 'stats.json', history_file = 'historyTotal.csv', train = True):
        """
        Playout the actual game between the two agents if they exist, otherwise raise an error
        Game loop iterates until a checkmate occurs
        """
        if self.agent1 is None or self.agent2 is None:
            raise ValueError('ERROR agent1 and agent2 can not be None for chessGame.play_out()')
        i = 0
        move_count = 0
        self.log('Game Started: {} as white, {} as black'.format(self.agent1.type,self.agent2.type))
        start = time.time()

        while not self.board.is_checkmate():
            try:
                move1 = self.agent1.make_move(depth = depth, board = self.board)
            except util.MCTSException as e:
                self.log(str(e))
                break
            if not move1 is None:
                 self.board.push(move1)
                 self.move_history.append({'state': self.board.fen(),'move1':move1})
            else:
                break
            
            # Now agent 2 selects and makes their move
            try:
                move2 = self.agent2.make_move(depth = depth, board = self.board)
            except util.MCTSException as e:
                self.log(str(e))
                break
            if not move2 is None:
                self.board.push(move2)
                self.move_history.append({'state': self.board.fen(),'move2':move2})
            else:
                break
            i+=1
            move_count += 1
            if move_count >= 200:
                break
            if (i >10):
                i = 0
                print('\n')

        end = time.time()
            
        exec_time = (end - start)

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
            self.winner = self.agent1.type
            print('Agent 1 Won!')
            self.agent1.write_data(history_file, did_win = 1)
            self.agent2.write_data(history_file, did_win = int(0))
        elif self.winner == Winner.BLACK:
            self.winner = self.agent2.type
            print('Agent 2 Won!')
            self.agent1.write_data(history_file, did_win = int(0))
            self.agent2.write_data(history_file, did_win = 1)
        else:
            self.winner = -1
            print('Draw!')
            #self.agent1.write_data('history.csv', did_win = int(0))
            #self.agent2.write_data('history.csv', did_win = int(0))

        sim_history = str(datetime.date.today()) + 'sim_history.log' 

        p = Path(util.HISTORY_DIR / sim_history)
        f = open(p,'a')
        for move in self.move_history:
            f.write(str(move))
            f.write('\n')
        f.write('END OF GAME, AGENT {} ({}) won\n'.format(self.winner, str(self.winner)))
        f.close()
        if train:
            self.update_total(exec_time)
            print('recorded stats')
        message = 'GAME OVER: {} as white, {} as black, {} won\n EXECUTION: {} seconds'.format(self.agent1.type,self.agent2.type,self.winner, exec_time)
        self.log(message = message)

    
    
    def log(self, message, msg_type=2):
        util.log(message, logger_str="game_play", msg_type=msg_type, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')

    
    def update_total(self, time = None, filename = 'stats.json'):
        with open(Path(util.HISTORY_DIR / filename), 'r') as f:
            totals = json.load(f)

        total_time = int(totals['Total Playing Time'])
        total_games = int(totals['Total Games'])
        total_games += 1
        totals['Total Games'] = total_games
        if not time is None:
            total_time += time
            totals['Total Playing Time'] = total_time

        with open(Path(util.HISTORY_DIR / 'stats.json'), 'w') as f:
            json.dump(totals, f)
    
    def get_winner(self):
        return self.winner
