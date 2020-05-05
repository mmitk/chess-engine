from pathlib import Path
import alphabeta as ab 
import markovsearch as mk
import chess 
from models import model as md
import util
from env import chessGame
import pandas as pd
import json

def update_vals(depth, num_wins, num_losses):
    # map of depths to key values in json file
    depth_map = {1:'Depth 1', 2: 'Depth 2', 3: 'Depth 3', 4: 'Depth 4', 5:'Depth 2'}

    with open(Path(util.HISTORY_DIR / 'test_stats.json'), 'r') as f:
        totals = json.load(f)

    # grab the depth to be updated
    stats_dict = totals[depth_map[depth]]
    stats_dict['Wins'] = int(stats_dict['Wins']) + num_wins
    stats_dict['Losses'] = int(stats_dict['Losses']) + num_losses

    with open(Path(util.HISTORY_DIR / 'test_stats.json'), 'w') as f:
        json.dump(totals, f)

def depth_1_test(model, eval_model, num_iter = 10):
    util.log('Testing depth 1 started', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    ab_agent = ab.alphabeta_agent()
    markov_agent = mk.markovagent(model = model,utilities_file = Path(util.HISTORY_DIR / 'updated_utility.json') ,eval_model = eval_model)
    games_won = {'Markov Agent': 0, 'Alphabeta Agent':0, 'Draw':0}

    for i in range(num_iter):
        print('#',end='')
        board = chess.Board()
        if i%2 == 0:
            white = ab_agent
            black = markov_agent 
        else:
            white = ab_agent
            black = markov_agent
        game = chessGame(white, black)
        game.set_board(board)
        game.play_out(history_file = 'test_depth_1.csv', train = False)

        winner = game.get_winner()

        # mark whether model based agent won
        if winner == markov_agent.type:
            games_won['Markov Agent'] += 1
        elif winner == ab_agent.type:
            games_won['Alphabeta Agent'] += 1

        # reset the game
        game.reset()
    print('\n')  
    update_vals(1,games_won['Markov Agent'],games_won['Alphabeta Agent'])
    util.log('COMPLETED: Testing depth 1', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')


def depth_2_test(model, eval_model,num_iter = 10):
    util.log('Testing depth 2 started', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    ab_agent = ab.alphabeta_agent()
    markov_agent = mk.markovagent(model = model,utilities_file = Path(util.HISTORY_DIR / 'updated_utility.json'), depth = 2,eval_model = eval_model )
    games_won = {'Markov Agent': 0, 'Alphabeta Agent':0, 'Draw':0}

    for i in range(num_iter):
        print('#',end='')
        board = chess.Board()
        if i%2 == 0:
            white = ab_agent
            black = markov_agent 
        else:
            white = ab_agent
            black = markov_agent
        game = chessGame(ab_agent, markov_agent)
        game.set_board(board)
        game.play_out(history_file = 'test_depth_2.csv', depth = 2, train = False)

        winner = game.get_winner()

        # mark whether model based agent won
        if winner == markov_agent.type:
            games_won['Markov Agent'] += 1
        elif winner == ab_agent.type:
            games_won['Alphabeta Agent'] += 1

        # reset the game
        game.reset()
    print('\n')      
    update_vals(2,games_won['Markov Agent'],games_won['Alphabeta Agent'])
    util.log('COMPLETED: Testing depth 2', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')


def depth_3_test(model, eval_model,num_iter = 10):
    util.log('Testing depth 3 started', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    ab_agent = ab.alphabeta_agent()
    markov_agent = mk.markovagent(model = model,utilities_file = Path(util.HISTORY_DIR / 'updated_utility.json'),depth = 3, eval_model = eval_model)
    games_won = {'Markov Agent': 0, 'Alphabeta Agent':0, 'Draw':0}

    for i in range(num_iter):
        print('#',end='')
        board = chess.Board()
        if i%2 == 0:
            white = ab_agent
            black = markov_agent 
        else:
            white = ab_agent
            black = markov_agent
        game = chessGame(ab_agent, markov_agent)
        game.set_board(board)
        game.play_out(history_file = 'test_depth_3.csv', depth = 3, train = False)

        winner = game.get_winner()

        # mark whether model based agent won
        if winner == markov_agent.type:
            games_won['Markov Agent'] += 1
        elif winner == ab_agent.type:
            games_won['Alphabeta Agent'] += 1

        # reset the game
        game.reset()
    print('\n')      
    update_vals(3,games_won['Markov Agent'],games_won['Alphabeta Agent'])
    util.log('COMPLETED: Testing depth 3', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')


def depth_4_test(model,eval_model, num_iter = 10):
    util.log('Testing depth 4 started', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')
    ab_agent = ab.alphabeta_agent()
    markov_agent = mk.markovagent(model = model,utilities_file = Path(util.HISTORY_DIR / 'updated_utility.json'), depth = 4 , eval_model = eval_model)
    games_won = {'Markov Agent': 0, 'Alphabeta Agent':0, 'Draw':0}

    for i in range(num_iter):
        print('#',end='')
        board = chess.Board()
        if i%2 == 0:
            white = ab_agent
            black = markov_agent 
        else:
            white = ab_agent
            black = markov_agent
        game = chessGame(ab_agent, markov_agent)
        game.set_board(board)
        game.play_out(history_file = 'test_depth_4.csv', depth = 4, train = False)

        winner = game.get_winner()

        # mark whether model based agent won
        if winner == markov_agent.type:
            games_won['Markov Agent'] += 1
        elif winner == ab_agent.type:
            games_won['Alphabeta Agent'] += 1

        # reset the game
        game.reset()
    print('\n')      
    update_vals(4,games_won['Markov Agent'],games_won['Alphabeta Agent'])
    util.log('COMPLETED: Testing depth 4', logger_str="train_sess", msg_type=2, write_to_console=False, path = util.HISTORY_DIR, filename = 'game_logs.log')

if __name__ == "__main__":
# retrain model to avoid version issues
    model = md.svm()
    prec = md.preprocessor()
    prec.fit(filename = Path(util.HISTORY_DIR / 'history3.csv'))
    data = prec.transform()
    model.fit(data)
    model.write_file(Path(util.HISTORY_DIR / 'model_3.pkl'))
    eval_model = md.svm(eval = True)
    data = pd.read_csv('models/history/raw_data.csv')
    eval_model.fit(data)
    depth_1_test(model,eval_model = eval_model,num_iter = 10)
    depth_2_test(model,eval_model = eval_model,num_iter = 10)
    depth_3_test(model,eval_model = eval_model,num_iter = 10)
    depth_4_test(model,eval_model = eval_model, num_iter =10)

