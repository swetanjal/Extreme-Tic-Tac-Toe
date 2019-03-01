######################## Version Headers ######################################################
import sys
import random
import signal
import time
import copy
import traceback

TIME = 24
MAX_PTS = 86
################################################################################################
class v3():
	def __init__(self):
		#self.board = BigBoard()
		self.cutoff_depth = 4
		self.my_symbol = 'x' # I am playing with symbol
		self.opp_symbol = 'o'
		self.inf = 1000000000000000000
		self.loss = -1000
		self.win = 1000
	
	def move(self, board, old_move, flag):
		self.board = copy.deepcopy(board)
		if flag == 'x':
			self.my_symbol = 'x'
			self.opp_symbol = 'o'
		else:
			self.my_symbol = 'o'
			self.opp_symbol = 'x'
		cells = board.find_valid_move_cells(old_move)
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
			if(bonus_move is True):
				val = self.minimax(0,move,alpha,beta)
			else:	
				val = self.minimax(1, move, alpha, beta)
				
			# Undo move
			self.board.big_boards_status[i][j][k] = '-'
			self.board.small_boards_status = temp

			bestVal = max(bestVal, val)
			if bestVal > alpha:
				alpha = bestVal
				best_move = move
			if beta <= alpha:
				break
		return best_move
	
	def check_small_board_win(self, n, row, col):
		"""
		This function returns whether I have won [row,col] small square in big board n
		"""
		
		# Indices in board array of the top left corner
		i = 3 * row
		j = 3 * col
		for tmp in range(3):
			if self.board.big_boards_status[n][i][j + tmp] == self.my_symbol and self.board.big_boards_status[n][i + 1][j + tmp] == self.my_symbol and self.board.big_boards_status[n][i + 2][j + tmp] == self.my_symbol:
				# Winning column
				return True
		for tmp in range(3):
			if self.board.big_boards_status[n][i + tmp][j] == self.my_symbol and self.board.big_boards_status[n][i + tmp][j + 1] == self.my_symbol and self.board.big_boards_status[n][i + tmp][j + 2] == self.my_symbol:
				# Winning row
				return True
		
		# Winning diagnol
		if self.board.big_boards_status[n][i][j] == self.my_symbol and self.board.big_boards_status[n][i + 1][j + 1] == self.my_symbol and self.board.big_boards_status[n][i + 2][j + 2] == self.my_symbol:
			return True
		
		if self.board.big_boards_status[n][i][j + 2] == self.my_symbol and self.board.big_boards_status[n][i + 1][j + 1] == self.my_symbol and self.board.big_boards_status[n][i + 2][j] == self.my_symbol:
			return True
		
		return False
    
	def check_small_board_loss(self, n, row, col):
		"""
		This function returns whether I have lost [row, col] small square in big board n
		"""
		# Indices in board array of the top left corner
		i = 3 * row
		j = 3 * col
		for tmp in range(3):
			if self.board.big_boards_status[n][i][j + tmp] == self.opp_symbol and self.board.big_boards_status[n][i + 1][j + tmp] == self.opp_symbol and self.board.big_boards_status[n][i + 2][j + tmp] == self.opp_symbol:
				# Winning column
				return True
		for tmp in range(3):
			if self.board.big_boards_status[n][i + tmp][j] == self.opp_symbol and self.board.big_boards_status[n][i + tmp][j + 1] == self.opp_symbol and self.board.big_boards_status[n][i + tmp][j + 2] == self.opp_symbol:
				# Winning row
				return True
		
		# Winning diagnol
		if self.board.big_boards_status[n][i][j] == self.opp_symbol and self.board.big_boards_status[n][i + 1][j + 1] == self.opp_symbol and self.board.big_boards_status[n][i + 2][j + 2] == self.opp_symbol:
			return True
		
		if self.board.big_boards_status[n][i][j + 2] == self.opp_symbol and self.board.big_boards_status[n][i + 1][j + 1] == self.opp_symbol and self.board.big_boards_status[n][i + 2][j] == self.opp_symbol:
			return True
		
		return False
    
    
	def heuristic(self):
		# Evaluate self.board
		############################################# MY SCORE #########################################################
		score = 0
		for i in range(2):
			for j in range(3):
				if self.check_small_board_loss(i, j, 0) and self.check_small_board_loss(i, j, 1) and self.check_small_board_loss(i, j, 2):
					return self.loss
			for j in range(3):
				if self.check_small_board_loss(i, 0, j) and self.check_small_board_loss(i, 1, j) and self.check_small_board_loss(i, 2, j):
					return self.loss
			if self.check_small_board_loss(i, 0, 0) and self.check_small_board_loss(i, 1, 1) and self.check_small_board_loss(i, 2, 2):
				return self.loss
			if self.check_small_board_loss(i, 0, 2) and self.check_small_board_loss(i, 1, 1) and self.check_small_board_loss(i, 2, 0):
				return self.loss
		
		for i in range(2):
			for j in range(3):
				if self.check_small_board_win(i, j, 0) and self.check_small_board_win(i, j, 1) and self.check_small_board_win(i, j, 2):
					return self.win
			for j in range(3):
				if self.check_small_board_win(i, 0, j) and self.check_small_board_win(i, 1, j) and self.check_small_board_win(i, 2, j):
					return self.win
			if self.check_small_board_win(i, 0, 0) and self.check_small_board_win(i, 1, 1) and self.check_small_board_win(i, 2, 2):
				return self.win
			if self.check_small_board_win(i, 0, 2) and self.check_small_board_win(i, 1, 1) and self.check_small_board_win(i, 2, 0):
				return self.win
		
		for i in range(2):
			for j in range(3):
				for k in range(3):
					res = self.check_small_board_win(i, j, k)
					if res:
						if j == 2 and k == 2:
							score = score + 3
						elif (j == 0 and k == 0) or (j == 0 and k == 2) or (j == 2 and k == 0) or (j ==2 and k == 2):
							score = score + 4
						else:
							score = score + 6
        ###################################################################################################################
		my_score = score
        ############################################# OPPONENT SCORE ########################################################
		score = 0
		for i in range(2):
			for j in range(3):
				for k in range(3):
					res = self.check_small_board_loss(i, j, k)
					if res:
						if j == 1 and k == 1:
							score = score + 3
						elif (j == 0 and k == 0) or (j == 0 and k == 2) or (j == 2 and k == 0) or (j ==2 and k == 2):
							score = score + 4
						else:
							score = score + 6
		#####################################################################################################################
		return (my_score - score)	
	
	def minimax(self, depth, old_move, alpha, beta):
		if self.board.find_terminal_state()[0] == self.my_symbol:
			return self.win
		if self.board.find_terminal_state()[0] == self.opp_symbol:
			return self.loss
		if depth == self.cutoff_depth:
			return self.heuristic()
		if depth % 2 == 0:
			# Maximizing Player
			bestVal = -self.inf
			cells = self.board.find_valid_move_cells(old_move)
			for move in cells:
				i = move[0]
				j = move[1]
				k = move[2]
				temp = copy.deepcopy(self.board.small_boards_status)
				bonus_move = self.board.update(old_move, move, self.my_symbol)[1]
				#self.board.big_boards_status[i][j][k] = self.my_symbol
				if bonus_move == True:
					bestVal = max(bestVal, self.minimax(depth, move, alpha, beta))
				else:
					bestVal = max(bestVal, self.minimax(depth + 1, move, alpha, beta))
					
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
				#self.board.big_boards_status[i][j][k] = self.opp_symbol
				if bonus_move == True:
					bestVal = min(bestVal, self.minimax(depth, move, alpha, beta))
				else:
					bestVal = min(bestVal, self.minimax(depth + 1, move, alpha, beta))
				
				# Undo move
				self.board.big_boards_status[i][j][k] = '-' 
				self.board.small_boards_status = temp

				beta = min(beta, bestVal)
				if beta <= alpha:
					break
			return bestVal
################################################################################################
