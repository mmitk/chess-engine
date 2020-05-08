Chess Engine built with a static evaluation and SVM

Training is done in train.py, different sessions set different oponents in order to ensure that there is variance
in the dataset.
Logs for training are found in scr/models/history

also in scr/models/history:

training datasets are:
    history.csv
    history2.csv
    history3.csv

Saved Models:
    All trained models are saved to .pkl files
    best performing model is test_model_2.pkl
    In order to see how to load a .pkl file into a model object see game.py line 252


Testing is done in test.py. Tests performed at depths 1-4 between SVM supported alphabeta agent (called the Markov Agent) and a
standard Monte Carlo Search Tree agent.
Unfortunately some of the testing logs were lost due to merging errors, but the ones that remain are also found in
src/models/history

DEMO:

in order to play against the demo:

    python game.py
(User is always the white pieces)

You may first need to set up a conda environment:

    conda env create -f env.yml


The stockfish-11-linux folder contains the open source stockfish software, and was used to gather training datasets

utility functions are located in util.py (log function, directory structures etc.)

The following files contain agents:
    markovsearch.py - contains the SVM driven model based chess agent, this is the main goal of the project
    alphabeta.py - contains a standard alphabeta search tree based agent using static evaluation function
    mcts.py - contains a standar monte carlo tree search based agent using static evaluation function 

The evaluation function is located in:

    env.py

In order to run the code in your own environment:

use spec-file.txt or env.yml to set up an anaconda environment

The test folder contains testing for data preprocessing and different ideas, some of which were not used 
