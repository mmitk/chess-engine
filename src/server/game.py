import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply


	return 0

if __name__ == '__main__':
	# run!
	app.run()