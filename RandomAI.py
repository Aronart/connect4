import numpy as np
from random import random
import AI
from Bitboard import *


class RandomAI(AI):
    def find_move(self, board, counter):
        _, _, height = process_board(board)
        possible_moves = list_moves(height)
        return random.choice(possible_moves)
