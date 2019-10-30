import numpy as np 
import random
from Prediction import getNNPrediction

class Board:

	def __init__(self):
		#Initialize board
		self.board = ['-' for i in range(0,9)]
		self.pastMoves = []
		self.winner = None


	def printBoard(self):
		#Print the Board
		print("\n Playing Board:")

		print(self.board[0], self.board[1], self.board[2])
		print(self.board[3], self.board[4], self.board[5])
		print(self.board[6], self.board[7], self.board[8])
		return

	def getAvailable(self):
		#returns list of available postions on the board
		moves = []
		for i,j in enumerate(self.board):
			if j == '-':
				moves.append(i)
		return moves

	def addMarker(self, marker, pos):
		#Adds player marker to the board

		self.board[pos] = marker
		self.pastMoves.append(pos)


	def lastMove(self):
		#Resets last move to '-' the empty marker
		self.board[self.pastMoves.pop()] = '-'
		self.winner = None

	def gameOver(self):
		#Checks if game has ended
		possibleWins = [(0,1,2),(3,4,5), (6,7,8), (0,3,6), (1,4,7),
						(2,5,8), (0,4,8),(2,4,6)]

		for i, j, k in possibleWins:
			if (self.board[i] == self.board[j] == self.board[k] 
				and self.board[i] != '-'):
				self.winner = self.board[i]
				return True

		if ('-' not in self.board):
			self.winner = '-'
			return True

		return False


	def playGame(self, p1, p2):
		#Play the game

		self.p1 = p1
		self.p2 = p2

		for i in range(9):
			self.printBoard()

			if( i % 2 == 0):
				if self.p1.type == 'H':
					print("\t\t[Human's Move]")
				else:
					print("\t\t[Computer's Move]")

				self.p1.move(self)

			else:
				if self.p2.type == 'H':
					print("\t\t[Human's Move]")
				else:
					print("\t\t[Computer's Move]")
				
				self.p2.move(self,self.board)

			if self.gameOver():
				self.printBoard()
				if self.winner == '-':
					print("\n It's a Tie!")
					#return 1
				else:
					print("Player %s Wins!" %self.winner)
					#if(self.winner == 'X'):
						#return 0
					#else:
						#return 2

				return

class Human:

	def __init__(self, marker):
		self.marker = marker
		self.type = 'H'

	def move(self, gameState):
		while True:
			m = input("Input position(1 - 9):")
			
			try:
				m = int(m) -1

			except:
				m = -1

			if m not in gameState.getAvailable():
				print("Invalid move. Try again.")

			else:
				break

		gameState.addMarker(self.marker, m)


class NeuralNet:

	def __init__(self, marker):
		self.marker = marker
		self.type = 'C'

		if self.marker == 'X':
			self.opponentmarker = 'O'
		else:
			self.opponentmarker = 'X'


	def move(self, gameState, board):
		#Convert board to numbers
		b = np.array([])
		for i in range(9):
			if board[i] == 'X':
				num = -1.00
			elif board[i] == 'O':
				num = 1.00
			else:
				num = 0.00
			b = np.append(b,num)
		#print(b)
		m = getNNPrediction(b)
		#print(m)
		optimalMove = m.argmax()
		#print(gameState.getAvailable())
		#Check if move is legal since NN is not 100% accurate. If recall the function
		if optimalMove not in gameState.getAvailable():
			print("Good Move!")
			bestScore = None
			posMoves = gameState.getAvailable()
			moves = np.zeros(shape=(len(posMoves), 2))
			for i in range(len(gameState.getAvailable())):
				num = posMoves[i]
				num2 = m[0][num]
				if bestScore == None or num2 > bestScore:
					bestScore = num2
					optimalMove = num
				

				#print(num2)
				#moves[i] =[num2,num]
				#print(moves[0])
			#optimalMove = moves.argmax()
			#(optimalMove)


		gameState.addMarker(self.marker, optimalMove)



#if __name__ == '__main__':

game = Board()
p1 = Human("X")
p2 = NeuralNet("O")
game.playGame(p1, p2)