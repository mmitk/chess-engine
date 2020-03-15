from pathlib import Path
import datetime
import time
import os
import argparse

DEBUG_LEVEL = 3
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
def log(message, logger_str=None, debug_level=5, filename=None, path=None, write_to_console=False):
    if debug_level < DEBUG_LEVEL:
        return
    print("LOGFILENAME:",  LOG_FILENAME)
    if not filename:
        if LOG_FILENAME:
            filename = LOG_FILENAME
        else:
            filename = str(datetime.date.today()) + '.log' # default filename
    if not path:
        path = Path(LOGS_DIR / filename) # default location is /data/logs/filename
    if logger_str:
        logger_str = "[" + str(logger_str) +"]"
    output = str(time.strftime("%H:%M:%S")) + str(logger_str) + ":\t" + message +'\n'
    try:
        with open(path, 'a') as f:
            f.write(output)
    except Exception:
        with open(path, 'w+') as f:
            f.write(output)
    if write_to_console:
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
    p.add_argument("-d", "--debug", "--debug-level", type=int, choices=range(1,6),help='sets the debug level, values should range from 1-5')
    p.add_argument("-l", "--log", nargs=1, help='pass a filename that you would like to direct log output to')

    args = p.parse_args()
    if args.debug:
        DEBUG_LEVEL = args.debug
        print(DEBUG_LEVEL)
    if args.log:
        global LOG_FILENAME
        LOG_FILENAME = str(args.log[0])
        print(LOG_FILENAME)

def type_parse_debug_level(string):
    v = int(string)
    if v < 1 or v > 5:
        msg = "Debug level argument %r is not between 1 and 5" % string
        raise argparse.ArgumentTypeError(msg)
    return v