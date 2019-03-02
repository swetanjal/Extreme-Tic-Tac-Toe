######################## Version Headers ######################################################
import sys
import random
import signal
import time
import copy
import traceback

TIME = 1000
MAX_PTS = 86
################################################################################################


class v6():
	def __init__(self):
		#self.board = BigBoard()
		self.cutoff_depth = 5
		self.cutoff_time = 15
		self.my_symbol = 'x'  # I am playing with symbol
		self.opp_symbol = 'o'
		self.inf = 1000000000000000000
		self.loss = -1000
		self.win = 1000
		self.curr_time = 0
		self.start_time = 0
		self.time_out = 0

	def move(self, board, old_move, flag):
		self.start_time = time.time()
		self.time_out = 0
		self.board = copy.deepcopy(board)
		if flag == 'x':
			self.my_symbol = 'x'
			self.opp_symbol = 'o'
		else:
			self.my_symbol = 'o'
			self.opp_symbol = 'x'
		cells = board.find_valid_move_cells(old_move)
		self.curr_time = time.time()
		self.cutoff_depth = 3
		best_move = []
		moves = []
		scores = []
		cons = 0
		if ( self.board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.my_symbol ):
			cons = 1

		while (self.curr_time - self.start_time) <= self.cutoff_time:
			alpha = -self.inf
			beta = self.inf
			bestVal = -self.inf
			best_move = []
			for move in cells:
				i = move[0]
				j = move[1]
				k = move[2]
				# self.board.big_boards_status[i][j][k] = self.my_symbol
				temp = copy.deepcopy(self.board.small_boards_status)
				bonus_move = self.board.update(old_move, move, self.my_symbol)[1]


				if(bonus_move is True and cons == 0):
					val = self.minimax(1, move, alpha, beta, 0, 1)
				else:
					val = self.minimax(1, move, alpha, beta, 1, 0)

				# Undo move
				self.board.big_boards_status[i][j][k] = '-'
				self.board.small_boards_status = temp

				bestVal = max(bestVal, val)
				if bestVal > alpha:
					alpha = bestVal
					best_move = move
				if beta <= alpha:
					break
			moves.append(best_move)
			scores.append(bestVal)
			self.cutoff_depth = self.cutoff_depth + 1
		l = len(moves)
		print scores
		if self.time_out == 1:
			return moves[l - 2]
		else:
			return moves[l - 1]


	def check_small_board_status(self,move):
		"""
		Function returns if this move results in a win of any small board , and return winning player symbol if so
		"""

		# Indices in board array of the top left corner
		x = move[1]/3
		x = x*3
		y = move[2]/3
		y = y*3
		k = move[0]

		board = self.board.big_boards_status[k]

		pos_x = move[1]%3
		pos_y = move[2]%3


        # Corner squares of the x,y'th small board
		if (pos_x%2) == 0 and (pos_y%2) == 0:

			# Rows of cell
			if board[x][y + pos_y] == board[x + 1][y + pos_y] and board[x + 1][y + pos_y] == board[x + 2][y + pos_y]:
				return board[x + pos_x][y + pos_y]

			# Column of cell
			if board[x + pos_x][y] == board[x + pos_x][y + 1] and board[x + pos_x][y + 1] == board[x + pos_x][y + 2]:
				return board[x + pos_x][y + pos_y]
            

			# Diagonal 1 (negative slope)
			if pos_x == pos_y:
				if board[x][y] == board[x + 1][y + 1] and board[x + 1][y + 1] == board[x + 2][y + 2]:
					return board[x + pos_x][y + pos_y]

			else:
				if (board[x][y+2] == board[x+1][y+1] and board[x+1][y+1] == board[x+2][y]):
					return board[x + pos_x][y + pos_y]

		# Edge squares
		if (pos_x + pos_y)%2 == 1:
			
			# Rows of cell
			if board[x][y + pos_y] == board[x + 1][y + pos_y] and board[x + 1][y + pos_y] == board[x + 2][y + pos_y]:
			    return board[x + pos_x][y + pos_y]

			# Column of cell
			if board[x + pos_x][y] == board[x + pos_x][y + 1] and board[x + pos_x][y + 1] == board[x + pos_x][y + 2]:
			    return board[x + pos_x][y + pos_y]

		# Centre Cell
		if (pos_x == 1 and pos_y ==1):

			# Rows of cell
			if board[x][y + pos_y] == board[x + 1][y + pos_y] and board[x + 1][y + pos_y] == board[x + 2][y + pos_y]:
			    return board[x + pos_x][y + pos_y]

			# Column of cell
			if board[x + pos_x][y] == board[x + pos_x][y + 1] and board[x + pos_x][y + 1] == board[x + pos_x][y + 2]:
			    return board[x + pos_x][y + pos_y]

			if board[x][y] == board[x + 1][y + 1] and board[x + 1][y + 1] == board[x + 2][y + 2]:
				return board[x + pos_x][y + pos_y]

			if (board[x][y+2] == board[x+1][y+1] and board[x+1][y+1] == board[x+2][y]):
				return board[x + pos_x][y + pos_y]
			

		return 'd'


	def heuristic(self,move):
		# Evaluate self.board
		score = 0

		win = self.check_small_board_status(move)
		if( win == self.my_symbol or win == self.opp_symbol):

			if(win == self.my_symbol):
				ret = self.win
			else:
				ret = self.loss


			# Indices in board array of the top left corner
			x = 0
			y = 0
			k = move[0]

			board = self.board.small_boards_status[k]

			pos_x = move[1]/3
			pos_y = move[2]/3


			# Corner squares of the x,y'th small board
			if (pos_x%2) == 0 and (pos_y%2) == 0:

				# Rows of cell
				if board[x][y + pos_y] == board[x + 1][y + pos_y] and board[x + 1][y + pos_y] == board[x + 2][y + pos_y]:
					return ret

				# Column of cell
				if board[x + pos_x][y] == board[x + pos_x][y + 1] and board[x + pos_x][y + 1] == board[x + pos_x][y + 2]:
					return ret
				

				# Diagonal 1 (negative slope)
				if pos_x == pos_y:
					if board[x][y] == board[x + 1][y + 1] and board[x + 1][y + 1] == board[x + 2][y + 2]:
						return ret

				else:
					if (board[x][y+2] == board[x+1][y+1] and board[x+1][y+1] == board[x+2][y]):
						return ret

			# Edge squares
			if (pos_x + pos_y)%2 == 1:
				
				# Rows of cell
				if board[x][y + pos_y] == board[x + 1][y + pos_y] and board[x + 1][y + pos_y] == board[x + 2][y + pos_y]:
					return ret

				# Column of cell
				if board[x + pos_x][y] == board[x + pos_x][y + 1] and board[x + pos_x][y + 1] == board[x + pos_x][y + 2]:
					return ret

			# Centre Cell
			if (pos_x == 1 and pos_y ==1):

				# Rows of cell
				if board[x][y + pos_y] == board[x + 1][y + pos_y] and board[x + 1][y + pos_y] == board[x + 2][y + pos_y]:
					return ret

				# Column of cell
				if board[x + pos_x][y] == board[x + pos_x][y + 1] and board[x + pos_x][y + 1] == board[x + pos_x][y + 2]:
					return ret

				if board[x][y] == board[x + 1][y + 1] and board[x + 1][y + 1] == board[x + 2][y + 2]:
					return ret

				if (board[x][y+2] == board[x+1][y+1] and board[x+1][y+1] == board[x+2][y]):
					return ret
		

		for i in range(2):
			for j in range(3):
				for k in range(3):
					res = self.board.small_boards_status[i][j][k]
					if res == self.my_symbol:
						if j == 1 and k == 1:
							score = score + 3
						elif (j == 0 and k == 0) or (j == 0 and k == 2) or (j == 2 and k == 0) or (j == 2 and k == 2):
							score = score + 4
						else:
							score = score + 6
					elif res == self.opp_symbol:
						if j == 1 and k == 1:
							score = score - 3
						elif (j == 0 and k == 0) or (j == 0 and k == 2) or (j == 2 and k == 0) or (j == 2 and k == 2):
							score = score - 4
						else:
							score = score - 6

		
		return score

	def minimax(self, depth, old_move, alpha, beta, turn, cons):

		if self.board.find_terminal_state()[0] == self.my_symbol:
			return self.win
		if self.board.find_terminal_state()[0] == self.opp_symbol:
			return self.loss
		self.curr_time = time.time()
		if depth == self.cutoff_depth or (self.curr_time - self.start_time) >= self.cutoff_time:
			self.time_out = 1
			return self.heuristic(old_move)
		if turn == 0:

			# Maximizing Player
			bestVal = -self.inf
			cells = self.board.find_valid_move_cells(old_move)
			for move in cells:
				i = move[0]
				j = move[1]
				k = move[2]
				temp = copy.deepcopy(self.board.small_boards_status)
				bonus_move = self.board.update(old_move, move, self.my_symbol)[1]
				if bonus_move == True and cons == 0:
					bestVal = max(bestVal, self.minimax(depth + 1, move, alpha, beta, turn, 1))
				else:
					bestVal = max(bestVal, self.minimax(depth + 1, move, alpha, beta, 1 - turn, 0))

				# Undo move
				self.board.big_boards_status[i][j][k] = '-'
				self.board.small_boards_status = temp

				alpha = max(alpha, bestVal)
				if beta <= alpha:
					break
			return bestVal
		else:
			# Minimizing Player
			bestVal = self.inf
			cells = self.board.find_valid_move_cells(old_move)
			for move in cells:
				i = move[0]
				j = move[1]
				k = move[2]
				temp = copy.deepcopy(self.board.small_boards_status)
				bonus_move = self.board.update(old_move, move, self.opp_symbol)[1]
				if bonus_move == True and cons == 0:
					bestVal = min(bestVal, self.minimax(depth + 1, move, alpha, beta, turn, 1))
				else:
					bestVal = min(bestVal, self.minimax(depth + 1, move, alpha, beta, 1 - turn, 0))

				# Undo move
				self.board.big_boards_status[i][j][k] = '-'
				self.board.small_boards_status = temp

				beta = min(beta, bestVal)
				if beta <= alpha:
					break
			return bestVal
################################################################################################
