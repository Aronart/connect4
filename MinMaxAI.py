import numpy as np
from AI import AI
from Bitboard import *


class MinMaxAI(AI):
    # cannot be 0
    max_depth = 1

    def __init__(self):
        # int in Python3 is equivalent to long in Python2
        # self.bitboards = np.array("i", [0, 0])
        # self.height = arr.array("i", [0, 7, 15, 24, 30, 35, 42])
        # self.height = None
        self.chosen_move = -1

    def find_move(self, board, counter):
        bitboards = np.array([0, 0], dtype=np.int64)
        bitboards[0], bitboards[1], height = process_board(board)
        self.min_max(bitboards, height, 0, -np.inf, np.inf, counter & 1)
        return self.chosen_move

    # player1 is maximizer
    def min_max(self, bitboards, height, depth, alpha, beta, player_index):
        #print(depth)
        if is_win(bitboards[player_index]):
            return np.inf
        elif depth == MinMaxAI.max_depth:
            # player_index ^ 1 is used because the previous player_index is evaluating the scores at this level
            heuristic = feature_score(bitboards, player_index ^ 1)
            return heuristic

        possible_moves = list_ordered_moves(height)
        '''# If no moves left, return an illegal move
        if len(possible_moves) == 0:
            pass
        '''
        if depth == 0:
            print(possible_moves)

        # maximizer
        if player_index == 0:
            value = -np.inf

            for col in possible_moves:
                bb_copy = np.array([bitboards[0], bitboards[1]], dtype=np.int64)
                h_copy = np.array([height[0], height[1], height[2], height[3], height[4], height[5], height[6]])

                # do the move
                make_move(bb_copy, h_copy, player_index, col)

                # value = max(value, self.min_max(bb_copy, h_copy, depth + 1, alpha, beta, 1))
                temp_value = self.min_max(bb_copy, h_copy, depth + 1, alpha, beta, 1)
                if temp_value > value:
                    value = temp_value
                    if depth == 0:
                        self.chosen_move = col

                alpha = max(alpha, value)

                if value >= beta:
                    break

            return value
        # minimizer
        else:
            value = np.inf

            for col in possible_moves:
                bb_copy = np.array([bitboards[0], bitboards[1]])
                h_copy = np.array([height[0], height[1], height[2], height[3], height[4], height[5], height[6]])

                # do the move
                make_move(bb_copy, h_copy, player_index, col)

                # value = min(value, self.min_max(bb_copy, h_copy, depth + 1, alpha, beta, 0))
                temp_value = self.min_max(bb_copy, h_copy, depth + 1, alpha, beta, 0)
                if temp_value < value:
                    value = temp_value
                    if depth == 0:
                        self.chosen_move = col

                beta = min(beta, value)

                if value <= alpha:
                    break

            return value
