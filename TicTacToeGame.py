import numpy as np 
import random

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
					#continue
					print("\t\t[Human's Move]")
				else:
					print("\t\t[Computer's Move]")
					
					with open('boardOptions.csv', 'a') as fd:
						for i in range(9):
							if self.board[i] == 'X':
								num = -1
							elif self.board[i] == 'O':
								num = 1
							else:
								num = 0
							fd.write(("%s," %str(num)))
						fd.write("\n")
				
				self.p2.move(self)

			if self.gameOver():
				self.printBoard()
				if self.winner == '-':
					print("\n It's a Tie!")
				else:
					print("Player %s Wins!" %self.winner)

				return

class Human:

	def __init__(self, marker):
		self.marker = marker
		self.type = 'H'

	def move(self, gameState):
		while True:
			#m = input("Input position:")
			#m = random.choice(gameState.getAvailable())
			try:
				m = int(m)

			except:
				m = -1

			if m not in gameState.getAvailable():
				print("Invalid move. Try again.")

			else:
				break

		gameState.addMarker(self.marker, m)


class MiniMax:

	def __init__(self, marker):
		self.marker = marker
		self.type = 'C'

		if self.marker == 'X':
			self.opponentmarker = 'O'
		else:
			self.opponentmarker = 'X'


	def move(self, gameState):
		move, score = self.maxMove(gameState)
		with open('bestMove.csv', 'a') as fd:
			fd.write(("%s \n" %str(move)))
		gameState.addMarker(self.marker, move)

	def maxMove(self, gameState):
		#Find max score
		bestScore = None
		bestMove = None

		for move in gameState.getAvailable():
			gameState.addMarker(self.marker, move)

			if gameState.gameOver():
				score = self.getScore(gameState)

			else:
				pos, score = self.minMove(gameState)

			gameState.lastMove()

			if bestScore == None or score > bestScore:
				bestScore = score
				bestMove = move

		return bestMove, bestScore

	def minMove(self, gameState):
		#Find min score
		bestScore = None
		bestMove = None

		for move in gameState.getAvailable():
			gameState.addMarker(self.opponentmarker, move)

			if gameState.gameOver():
				score = self.getScore(gameState)

			else:
				pos, score = self.maxMove(gameState)

			gameState.lastMove()

			if bestScore == None or score < bestScore:
				bestScore = score
				bestMove = move

		return bestMove, bestScore

	def getScore(self, gameState):
		if gameState.gameOver():
			if gameState.winner == self.marker:
				return 10 
			elif gameState.winner == self.opponentmarker:
				return -10

		return 0


#if __name__ == '__main__':
#for _ in range(10000):
game = Board()
p1 = Human("X")
p2 = MiniMax("O")
game.playGame(p1, p2)



















