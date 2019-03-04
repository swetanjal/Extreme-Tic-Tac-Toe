######################## Version Headers ######################################################
#import sys
import random
#import signal
import time
import copy
#import traceback

#TIME = 24
#MAX_PTS = 86
################################################################################################


class Team33():
	def __init__(self):
		#self.board = BigBoard()
		self.cutoff_depth = 4
		self.cutoff_time = 18
		self.my_symbol = 'x'  # I am playing with symbol
		self.opp_symbol = 'o'
		self.inf = long(1000000000000000000)
		self.loss = long(-1 * 100000000)
		self.win = long(100000000)
		self.curr_time = 0
		self.start_time = 0
		self.time_out = 0

		self.randBigBoard = [[[[long(0) for l in range(2)]for k in range(9)]for j in range(9)]for i in range(2)]
		self.hashScore = {}
		self.hashVal = 0
		self.hash_init()


	def hash_init(self):
		for i in range(2):
			for j in range(9):
				for k in range(9):
					for l in range(2):
						self.randBigBoard[i][j][k][l] = long(random.randint(3, 2 ** 64))


	def move(self, board, old_move, flag):

		if(old_move[0] == -1 and old_move[1] == -1 and old_move[2] == -1):
			print old_move
			return (0,4,4)
		self.start_time = time.time()
		self.time_out = 0
		self.board = copy.deepcopy(board)
		if flag == 'x':
			self.my_symbol = 'x'
			self.opp_symbol = 'o'
		else:
			self.my_symbol = 'o'
			self.opp_symbol = 'x'
		############ Hashing ##############
		self.hashVal = 0
		for i in range(2):
			for j in range(9):
				for k in range(9):
					if self.board.big_boards_status[i][j][k] == self.my_symbol:
						self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][0]
					elif self.board.big_boards_status[i][j][k] == self.opp_symbol:
						self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][1]
		###################################
		cells = board.find_valid_move_cells(old_move)
		self.curr_time = time.time()
		self.cutoff_depth = 3
		best_move = []
		moves = []
		scores = []
		cons = 0
		if (self.board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.my_symbol ):
			cons = 1

		while (self.curr_time - self.start_time) <= self.cutoff_time:
			alpha = -self.inf
			beta = self.inf
			bestVal = -self.inf
			best_move = []


			for move in cells:

				now = time.time()

				if (now - self.start_time) >= self.cutoff_time:
					self.time_out = 1
					break


				if(len(self.hashScore) > 1000000):
					self.hashScore = {}


				i = move[0]
				j = move[1]
				k = move[2]
				# self.board.big_boards_status[i][j][k] = self.my_symbol
				temp = copy.deepcopy(self.board.small_boards_status)
				bonus_move = self.board.update(old_move, move, self.my_symbol)[1]


				self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][0]

				if(bonus_move is True and cons == 0):
					val = self.minimax(1, move, alpha, beta, 0, 1)
				else:
					val = self.minimax(1, move, alpha, beta, 1, 0)

				# Undo move
				self.board.big_boards_status[i][j][k] = '-'
				self.board.small_boards_status = temp
				self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][0]
				bestVal = max(bestVal, val)

				# if bestVal == self.win:
				# 	return move

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
		print moves

		if self.time_out == 1:
			if moves[l - 2] == []:
				print '-----------------------HAPPENED---------------------'
				return moves[0]
			else:
				return moves[l-2]
		
		else:
			return moves[l - 1]



	def small_block_eval(self, board, sym , opp):

		v_flag = True
		h_flag = True
		h_count = 0
		v_count = 0
		score = 0

		for i in range(3):
			v_flag = True
			h_flag = True
			h_count = 0
			v_count = 0


			for j in range(3):
				if(board[i][j] == sym):
					h_count = h_count + 1

				elif(board[i][j] == opp):
					h_flag = False

				if(board[j][i] == sym):
					v_count = v_count + 1
				elif(board[j][i] == opp):
					v_flag = False

			if(v_flag):
				if(v_count == 3):
					score = score + 100
				elif(v_count == 2):
					score = score + 20
				elif(v_count == 1):
					score = score + 5

			if(h_flag):
				if(h_count == 3):
					score = score + 100
				elif(h_count == 2):
					score = score + 20
				elif(h_count == 1):
					score = score + 5



		d_flag = True
		d_count = 0

		for i in range(3):
			if (board[i][i] == sym):
				d_count = d_count + 1
			elif(board[i][i] == opp):
				d_flag = False

		if(d_flag):
			if(d_count == 3):
				score = score + 100
			elif(d_count == 2):
				score = score + 20
			elif(d_count == 1):
				score = score + 5

		d_flag = True
		d_count = 0

		for i in range(3):
			if (board[i][2 - i] == sym):
				d_count = d_count + 1
			elif(board[i][2 - i] == opp):
				d_flag = False

		if(d_flag):
			if(d_count == 3):
				score = score + 100
			elif(d_count == 2):
				score = score + 20
			elif(d_count == 1):
				score = score + 5

		return score 



	def slice(self, board_no, start_row, end_row, start_col, end_col):
		res = []
		for i in range(start_row, end_row):
			lis = []
			for j in range(start_col, end_col):
				lis.append(self.board.big_boards_status[board_no][i][j])
			res.append(lis)

		return res


	def heuristic(self,move):
		# Evaluate self.board

		self.curr_time = time.time()
		if ((self.curr_time - self.start_time) >= self.cutoff_time):
			return 0


		score = 0
		if self.hashVal in self.hashScore:
			return self.hashScore[self.hashVal]

		for k in range(2):
			for i in range(3):
				for j in range(3):
					if(self.board.small_boards_status[k][i][j] == '-'):
						temp = self.slice(k,i*3,(i+1)*3,j*3,(j+1)*3)
						score = score + (0.1)*self.small_block_eval(temp , self.my_symbol,self.opp_symbol)
						score = score - (0.1)*self.small_block_eval(temp , self.opp_symbol,self.my_symbol)




		local_score = 0
		for k in range(2):

			board = []
			for i in range(0, 3):
				lis = []
				for j in range(0, 3):
					lis.append(self.board.small_boards_status[k][i][j])
				board.append(lis)


			v_flag = True
			h_flag = True
			h_count = 0
			v_count = 0

			for i in range(3):
				v_flag = True
				h_flag = True
				h_count = 0
				v_count = 0


				for j in range(3):

					if(board[i][j] == self.my_symbol):
						h_count = h_count + 1

					elif(board[i][j] == self.opp_symbol):
						h_flag = False

					if(board[j][i] == self.my_symbol):
						v_count = v_count + 1

					elif(board[j][i] == self.opp_symbol):
						v_flag = False


					if(v_flag):
						if(v_count == 3):
							local_score = local_score + 100 + 10
						elif(v_count == 2):
							local_score = local_score + 20 + 10
						elif(v_count == 1):
							local_score = local_score + 5 + 10

					elif(not v_flag):
						if(v_count == 3):
							local_score = local_score + 100
						elif(v_count == 2):
							local_score = local_score + 20
						elif(v_count == 1):
							local_score = local_score + 5




					if(h_flag):
						if(h_count == 3):
							local_score = local_score + 100 + 10
						elif(h_count == 2):
							local_score = local_score + 20 + 10
						elif(h_count == 1):
							local_score = local_score + 5 + 10

					elif(not h_flag):
						if(h_count == 3):
							local_score = local_score + 100
						elif(h_count == 2):
							local_score = local_score + 20
						elif(h_count == 1):
							local_score = local_score + 5


			d_flag = True
			d_count = 0

			for i in range(3):
				if (board[i][i] == self.my_symbol):
					d_count = d_count + 1
				elif(board[i][i] == self.opp_symbol):
					d_flag = False

			if(d_flag):
				if(d_count == 3):
					local_score = local_score + 100 + 10
				elif(d_count == 2):
					local_score = local_score + 20 + 10
				elif(d_count == 1):
					local_score = local_score + 5 + 10

			elif(not d_flag):
				if(d_count == 3):
					local_score = local_score + 100 
				elif(d_count == 2):
					local_score = local_score + 20
				elif(d_count == 1):
					local_score = local_score + 5

			d_flag = True
			d_count = 0

			for i in range(3):
				if (board[i][2 - i] == self.my_symbol):
					d_count = d_count + 1
				elif(board[i][2 - i] == self.opp_symbol):
					d_flag = False

			if(d_flag):
				if(d_count == 3):
					local_score = local_score + 100 + 10
				elif(d_count == 2):
					local_score = local_score + 20 + 10
				elif(d_count == 1):
					local_score = local_score + 5 + 10

			elif(not d_flag):
				if(d_count == 3):
					local_score = local_score + 100 
				elif(d_count == 2):
					local_score = local_score + 20
				elif(d_count == 1):
					local_score = local_score + 5


		score = score + 30 * local_score


		local_score = 0
		for k in range(2):

			board = []
			for i in range(0, 3):
				lis = []
				for j in range(0, 3):
					lis.append(self.board.small_boards_status[k][i][j])
				board.append(lis)


			v_flag = True
			h_flag = True
			h_count = 0
			v_count = 0

			for i in range(3):
				v_flag = True
				h_flag = True
				h_count = 0
				v_count = 0


				for j in range(3):

					if(board[i][j] == self.opp_symbol):
						h_count = h_count + 1

					elif(board[i][j] == self.my_symbol):
						h_flag = False

					if(board[j][i] == self.opp_symbol):
						v_count = v_count + 1

					elif(board[j][i] == self.my_symbol):
						v_flag = False


					if(v_flag):
						if(v_count == 3):
							local_score = local_score + 100 + 10
						elif(v_count == 2):
							local_score = local_score + 20 + 10
						elif(v_count == 1):
							local_score = local_score + 5 + 10

					elif(not v_flag):
						if(v_count == 3):
							local_score = local_score + 100
						elif(v_count == 2):
							local_score = local_score + 20
						elif(v_count == 1):
							local_score = local_score + 5




					if(h_flag):
						if(h_count == 3):
							local_score = local_score + 100 + 10
						elif(h_count == 2):
							local_score = local_score + 20 + 10
						elif(h_count == 1):
							local_score = local_score + 5 + 10

					elif(not h_flag):
						if(h_count == 3):
							local_score = local_score + 100
						elif(h_count == 2):
							local_score = local_score + 20
						elif(h_count == 1):
							local_score = local_score + 5


			d_flag = True
			d_count = 0

			for i in range(3):
				if (board[i][i] == self.opp_symbol):
					d_count = d_count + 1
				elif(board[i][i] == self.my_symbol):
					d_flag = False

			if(d_flag):
				if(d_count == 3):
					local_score = local_score + 100 + 10
				elif(d_count == 2):
					local_score = local_score + 20 + 10
				elif(d_count == 1):
					local_score = local_score + 5 + 10

			elif(not d_flag):
				if(d_count == 3):
					local_score = local_score + 100 
				elif(d_count == 2):
					local_score = local_score + 20
				elif(d_count == 1):
					local_score = local_score + 5

			d_flag = True
			d_count = 0

			for i in range(3):
				if (board[i][2 - i] == self.opp_symbol):
					d_count = d_count + 1
				elif(board[i][2 - i] == self.my_symbol):
					d_flag = False

			if(d_flag):
				if(d_count == 3):
					local_score = local_score + 100 + 10
				elif(d_count == 2):
					local_score = local_score + 20 + 10
				elif(d_count == 1):
					local_score = local_score + 5 + 10

			elif(not d_flag):
				if(d_count == 3):
					local_score = local_score + 100 
				elif(d_count == 2):
					local_score = local_score + 20
				elif(d_count == 1):
					local_score = local_score + 5


		score = score - 30 * local_score



		for k in range(2):
			for i in range(9):
				for j in range(9):
					pos_x = i%3
					pos_y = j%3
					if(self.board.big_boards_status[k][i][j] == self.my_symbol):
						# Corner
						if(pos_x%2 == 0 and pos_y%2 == 0):
							score = score + 0.002

						# Centre
						elif(pos_y == 1 and pos_y == 1):
							score = score + 0.005
		
		self.hashScore[self.hashVal] = score
		return score



	def minimax(self, depth, old_move, alpha, beta, turn, cons):

		if self.board.find_terminal_state()[0] == self.my_symbol:
			return self.win*(165 - depth)
		if self.board.find_terminal_state()[0] == self.opp_symbol:
			return self.loss*(165 - depth)



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
				self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][0]
				temp = copy.deepcopy(self.board.small_boards_status)
				bonus_move = self.board.update(old_move, move, self.my_symbol)[1]
				if bonus_move == True and cons == 0:
					bestVal = max(bestVal, self.minimax(depth + 1, move, alpha, beta, turn, 1))
				else:
					bestVal = max(bestVal, self.minimax(depth + 1, move, alpha, beta, 1 - turn, 0))

				# Undo move
				self.board.big_boards_status[i][j][k] = '-'
				self.board.small_boards_status = temp
				self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][0]
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
				self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][1]
				if bonus_move == True and cons == 0:
					bestVal = min(bestVal, self.minimax(depth + 1, move, alpha, beta, turn, 1))
				else:
					bestVal = min(bestVal, self.minimax(depth + 1, move, alpha, beta, 1 - turn, 0))

				# Undo move
				self.board.big_boards_status[i][j][k] = '-'
				self.board.small_boards_status = temp
				self.hashVal = self.hashVal ^ self.randBigBoard[i][j][k][1]
				beta = min(beta, bestVal)
				if beta <= alpha:
					break
			return bestVal
################################################################################################
