import numpy as np


# bitboard operations adapted from https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
def process_board(board):
    bitboard1, bitboard2 = '', ''
    height = np.array("i", [0, 7, 15, 24, 30, 35, 42])
    # Start with right-most column
    for j in range(6, -1, -1):
        # Add 0-bits to sentinel
        bitboard1 += '0'
        bitboard2 += '0'

        height_added = False
        # Start with top row
        for i in range(0, 6):
            player_stone = board[i, j]
            if player_stone == 0:
                bitboard1 += '0'
                bitboard2 += '0'
            else:
                if player_stone == 1:
                    bitboard1 += '1'
                    bitboard2 += '0'
                # player_stone == 2
                else:
                    bitboard1 += '0'
                    bitboard2 += '1'

                if not height_added:
                    height[j] += 6 - i
                    height_added = True

    return int(bitboard1, 2), int(bitboard2, 2), height


def make_move(bitboards, height, player_index, column):
    move = 1 << height[column]
    height[column] += 1
    bitboards[player_index] ^= move
    # moves[counter] = column
    # counter += 1


def is_win(bitboard):
    directions = [1, 7, 6, 8]
    for direction in directions:
        bb = bitboard & (bitboard >> direction)
        if bb & (bb >> (2 * direction)) != 0:
            return True
    return False


def list_moves(height):
    possible_moves = []
    top = 0b1000000_1000000_1000000_1000000_1000000_1000000_1000000
    cols = 7
    for col in range(cols):
        if top & (1 << height[col]) == 0:
            possible_moves.append(col)
    return possible_moves


def list_ordered_moves(height):
    possible_moves = []
    col_order = [3, 2, 4, 1, 5, 0, 6]
    top = 0b1000000_1000000_1000000_1000000_1000000_1000000_1000000
    for col in col_order:
        if top & (1 << height[col]) == 0:
            possible_moves.append(col)
    return possible_moves
