from keras.models import load_model
import numpy as np 


def getNNPrediction(board):
	model = load_model('model.TicTacToe')

	#convert board so that it fits the data the Neural Net expects (9, )
	npBoard = np.array([board])

	pred = model.predict(npBoard)
	return pred