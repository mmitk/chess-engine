from pathlib import Path
from enum import IntEnum
import chess
import datetime
import time
import os
import argparse

class LogMessage(IntEnum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

DEBUG_LEVEL = LogMessage.DEBUG
CONSOLE_DEBUG_LEVEL = LogMessage.WARNING
CONSOLE_OUTPUT = False

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent # get root of project
DATA_DIR = Path(ROOT_DIR / "data")
HISTORY_DIR = Path(DATA_DIR / "history")
MODELS_DIR = Path(DATA_DIR / "models")
LOGS_DIR = Path(DATA_DIR / "logs")
LOG_FILENAME = ""


"""
Initiate directories. If they exist (as expected), nothing happens, if they don't they are created.
"""
def init_data_dirs():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(HISTORY_DIR).mkdir(parents=True, exist_ok=True)
    Path(MODELS_DIR).mkdir(parents=True, exist_ok=True)
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)


"""
message == msg to be printed to logfile
logger_str == a prefix that could indicate what fn/object is calling the log function. by default won't print anything
debug_level == indicates level of importance of message. 
filename == if we wanted a different filename or to pass a path
path == if we wanted to save to a different dirpath
write_to_console == exactly what it sounds like. Boolean T/F.
if we wanted to print fewer messages we could lower the debug level. Level would be 1-5, 
where 1 is of lowest importance, 5 is of highest. Ideally need to implement way to get debug level from user,
and alter logging as a result 
"""
def log(message, logger_str=None, msg_type=LogMessage.DEBUG, filename=None, path=None, write_to_console=False):
    global DEBUG_LEVEL
    if isinstance(msg_type, int):
        if msg_type > 5 or msg_type < 1:
            raise ValueError("msg_type must be LogMessage member or int value between 1 and 5")
        else:
            msg_type = LogMessage(msg_type)
    if msg_type < DEBUG_LEVEL and msg_type < CONSOLE_DEBUG_LEVEL:
        return
    global LOG_FILENAME
    global CONSOLE_OUTPUT
    if not filename:
        if LOG_FILENAME:
            filename = LOG_FILENAME
        else:
            filename = str(datetime.date.today()) + '.log' # default filename
            LOG_FILENAME = filename
    if not path:
        path = Path(LOGS_DIR / filename) # default location is /data/logs/filename
    if logger_str:
        logger_str = "[" + str(logger_str) +"]"
    output = str(time.strftime("%H:%M:%S:")) + msg_type.name + ":" + str(logger_str) + ":" + message +'\n'
    try:
        with open(path, 'a') as f:
            f.write(output)
    except Exception:
        with open(path, 'w+') as f:
            f.write(output)
    if write_to_console is None:
        if CONSOLE_OUTPUT and CONSOLE_DEBUG_LEVEL <= msg_type:
            print(output)

"""
Argparse:
this function should create a parser object, add arguments, and return it to a function in game.py where parse_args will be called

* setting debug level [-d](1-5): -d [1-5]
* logfile related [-l]- potential options:
-ln == create new logfile for this run 
-lo == output filename for the log? (if exists: app, else: w+ )
* enabling/disabling console output messages (perhaps create CONSOLE_DEBUG_LVL and LOG_DEBUG_LVL)
"""
def parse_cmd_line():
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--debug", "--debug-level", nargs=1, type=int, choices=range(1,6), help='sets the debug level, values should range from 1-5')
    p.add_argument("-l", "--log", nargs=1, help='pass a filename that you would like to direct log output to')
    p.add_argument("-c", "--console", nargs='?',type=str_to_bool, help='enables/disables console output, default=false')
    args = p.parse_args()
    global CONSOLE_OUTPUT
    
    if args.debug:
        global DEBUG_LEVEL
        DEBUG_LEVEL = LogMessage(args.debug[0])
    if args.log:
        global LOG_FILENAME
        LOG_FILENAME = str(args.log[0])
    if args.console:
        global CONSOLE_OUTPUT
        CONSOLE_OUTPUT = True

def str_to_bool(v):
    global CONSOLE_OUTPUT
    if isinstance(v, bool):
        CONSOLE_OUTPUT = v
        return
    i = int(v)
    if 1 <= i <= 5:
        global CONSOLE_DEBUG_LEVEL
        CONSOLE_DEBUG_LEVEL = LogMessage(i)
        CONSOLE_OUTPUT = True
        return
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        CONSOLE_OUTPUT = True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        CONSOLE_OUTPUT = False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected')


def bin_matrix_to_decimal(matrix):
    m = matrix.reshape(-1)
    dec = 0
    j = 0
    for i in range(len(m)-1):
        if m[i]:
            dec += 2**j
        j += 1
    return float(dec)


def serialize(board):
    import numpy as np
    assert board.is_valid()

    bstate = np.zeros(64, np.uint8)
    for i in range(64):
      pp = board.piece_at(i)
      if pp is not None:
        #print(i, pp.symbol())
        bstate[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6, \
                     "p": 9, "n":10, "b":11, "r":12, "q":13, "k": 14}[pp.symbol()]
    if board.has_queenside_castling_rights(chess.WHITE):
      assert bstate[0] == 4
      bstate[0] = 7
    if board.has_kingside_castling_rights(chess.WHITE):
      assert bstate[7] == 4
      bstate[7] = 7
    if board.has_queenside_castling_rights(chess.BLACK):
      assert bstate[56] == 8+4
      bstate[56] = 8+7
    if board.has_kingside_castling_rights(chess.BLACK):
      assert bstate[63] == 8+4
      bstate[63] = 8+7

    if board.ep_square is not None:
      assert bstate[self.board.ep_square] == 0
      bstate[self.board.ep_square] = 8
    bstate = bstate.reshape(8,8)


    state = []
   
    state.append(bin_matrix_to_decimal((bstate>>3)&1))
    state.append(bin_matrix_to_decimal((bstate>>2)&1))
    state.append(bin_matrix_to_decimal((bstate>>1)&1))
    state.append(bin_matrix_to_decimal((bstate>>0)&1))

    state.append(board.turn*1.0)
    
    return state
