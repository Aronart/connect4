import numpy as np


# bitboard operations adapted from https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
def process_board(board):
    bitboard1, bitboard2 = '', ''
    height = np.array([0, 7, 14, 21, 28, 35, 42])
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

    print(bitboard1)
    print(bitboard2)
    print(height)
    return int(bitboard1, 2), int(bitboard2, 2), height


def make_move(bitboards, height, player_index, column):
    move = np.int64(1) << height[column]
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
        if top & (np.int64(1) << height[col]) == 0:
            possible_moves.append(col)
    return possible_moves


def list_ordered_moves(height):
    possible_moves = []
    col_order = [3, 2, 4, 1, 5, 0, 6]
    top = 0b1000000_1000000_1000000_1000000_1000000_1000000_1000000
    for col in col_order:
        #print(col)
        #print("{0:b}".format(top))
        #print("{0:b}".format((np.int64(1) << height[col])))
        if ~top & (np.int64(1) << height[col]):
            possible_moves.append(col)
    return possible_moves


def num_bin_ones(bin):
    num = 0
    while(bin):
        num += 1
        bin &= bin - 1
    return num


def feature_score(bitboards, player_index):
    player_bb = bitboards[player_index]
    adj_mask = bitboards[0] | bitboards[1] | 0b1111111_1111111_1000000_1000000_1000000_1000000_1000000_1000000_1000000
    bottom = 0b0000001_0000001_0000001_0000001_0000001_0000001_0000001
    # left = 0b0000000_0000000_0000000_0000000_0000000_0000000_1111111
    final_score = 0
    score1 = np.inf
    score2 = 900_000
    score3 = 50_000
    score4 = 40_000
    score5 = 30_000
    score6 = 20_000
    score7 = 10_000

    # 3 stones
    # with free spaces directly on right and left side
    # also checking that one can immediately place a stone in both of the side spaces (on the bottom row or a stone below) if they are empty

    # horizontal
    if player_bb >> 7 & player_bb >> 14 & player_bb >> 21 & ~adj_mask & ~(adj_mask >> 28) & (adj_mask << 1 | bottom) & (adj_mask >> 27 | bottom >> 28):
        return score1
    # diagonal \
    elif player_bb >> 6 & player_bb >> 12 & player_bb >> 18 & ~adj_mask & ~(adj_mask >> 24) & adj_mask << 1 & (adj_mask >> 23 | bottom >> 24):
        return score1
    # diagonal /
    elif player_bb >> 8 & player_bb >> 16 & player_bb >> 24 & ~adj_mask & ~(adj_mask >> 32) & (adj_mask << 1 | bottom) & adj_mask >> 31:
        return score1

    # 3 stones vertical checked separately
    temp_bb = player_bb & (player_bb >> 1) & (player_bb >> 2) & ~(adj_mask >> 3)
    if temp_bb:
        final_score += score2 * num_bin_ones(temp_bb)

    # 3 stones (not necessarily connected)
    # with one stone missing anywhere to make 4 connected stones
    # not checking if one can immediately put a stone in the empty space
    directions = [7, 6, 8]
    for direction in directions:
        temp_bb = ~adj_mask & player_bb >> direction & player_bb >> (2 * direction) & player_bb >> (3 * direction)
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)
        temp_bb = player_bb & ~(adj_mask >> direction) & player_bb >> (2 * direction) & player_bb >> (3 * direction)
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)
        temp_bb = player_bb & player_bb >> direction & ~(adj_mask >> (2 * direction)) & player_bb >> (3 * direction)
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)
        temp_bb = player_bb & player_bb >> direction & player_bb >> (2 * direction) & ~(adj_mask >> (3 * direction))
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)

    # 2 stones
    # with free spaces directly on right and left side
    # not checking if one can immediately put a stone in the empty spaces

    # horizontal
    temp_bb = player_bb >> 7 & player_bb >> 14 & ~adj_mask & ~(adj_mask >> 21)
    if temp_bb:
        final_score += score3 * num_bin_ones(temp_bb)
    # diagonal \
    temp_bb = player_bb >> 6 & player_bb >> 12 & ~adj_mask & ~(adj_mask >> 18)
    if temp_bb:
        final_score += score3 * num_bin_ones(temp_bb)
    # diagonal /
    temp_bb = player_bb >> 8 & player_bb >> 16 & ~adj_mask & ~(adj_mask >> 24)
    if temp_bb:
        final_score += score3 * num_bin_ones(temp_bb)

    # 2 stones
    # where a move can be made on an immediately adjacent column
    # The value depends on the number of available squares along a direction until an unavailable square is met

    directions = [1, 7, 6, 8]
    for direction in directions:
        # check on right
        temp_bb = player_bb & player_bb >> direction & ~(adj_mask >> (2 * direction)) & ~(adj_mask >> (3 * direction)) & ~(adj_mask >> (4 * direction)) & ~(adj_mask >> (5 * direction)) & ~(adj_mask >> (6 * direction))
        if temp_bb:
            final_score += score4 * num_bin_ones(temp_bb)
        # ^= prevents recounting the 5 empty spaces in a chain
        temp_bb ^= player_bb & player_bb >> direction & ~(adj_mask >> (2 * direction)) & ~(adj_mask >> (3 * direction)) & ~(adj_mask >> (4 * direction)) & ~(adj_mask >> (5 * direction))
        if temp_bb:
            final_score += score5 * num_bin_ones(temp_bb)
        temp_bb ^= player_bb & player_bb >> direction & ~(adj_mask >> (2 * direction)) & ~(adj_mask >> (3 * direction)) & ~(adj_mask >> (4 * direction))
        if temp_bb:
            final_score += score6 * num_bin_ones(temp_bb)
        temp_bb ^= player_bb & player_bb >> direction & ~(adj_mask >> (2 * direction)) & ~(adj_mask >> (3 * direction))
        if temp_bb:
            final_score += score7 * num_bin_ones(temp_bb)

        # check on left
        temp_bb = ~adj_mask & ~(adj_mask >> direction) & ~(adj_mask >> (2 * direction)) & ~(adj_mask >> (3 * direction)) & ~(adj_mask >> (4 * direction)) & player_bb >> (5 * direction) & player_bb >> (6 * direction)
        if temp_bb:
            final_score += score4 * num_bin_ones(temp_bb)
        # ^= prevents recounting the 5 empty spaces in a chain
        temp_bb ^= (~adj_mask & ~(adj_mask >> direction) & ~(adj_mask >> (2 * direction)) & ~(adj_mask >> (3 * direction)) & player_bb >> (4 * direction) & player_bb >> (5 * direction)) >> direction
        if temp_bb:
            final_score += score5 * num_bin_ones(temp_bb)
        temp_bb ^= (~adj_mask & ~(adj_mask >> direction) & ~(adj_mask >> (2 * direction)) & player_bb >> (3 * direction) & player_bb >> (4 * direction)) >> direction
        if temp_bb:
            final_score += score6 * num_bin_ones(temp_bb)
        temp_bb ^= (~adj_mask & ~(adj_mask >> direction) & player_bb >> (2 * direction) & player_bb >> (3 * direction)) >> direction
        if temp_bb:
            final_score += score7 * num_bin_ones(temp_bb)

    # 1 stone
    # that is not connected to another same chessman horizontally, vertically or diagonally
    temp_bb = player_bb & ~(player_bb >> 1) & ~(player_bb >> 8) & ~(player_bb >> 7) & ~(player_bb >> 6) & ~(player_bb << 1) & ~(player_bb << 8) & ~(player_bb << 7) & ~(player_bb << 6)
    if temp_bb:
        final_score += single_stone_points(temp_bb)

    # the heuristic final score should be negative if we are the minimizer
    if player_index & 1:
        final_score *= -1

    return final_score


def single_stone_points(bin):
    temp_score = 0
    col1 = 0b0000000_0000000_0000000_1111111_0000000_0000000_0000000
    cols2 = 0b0000000_0000000_1111111_0000000_1111111_0000000_0000000
    cols3 = 0b0000000_1111111_0000000_0000000_0000000_1111111_0000000
    cols4 = 0b1111111_0000000_0000000_0000000_0000000_0000000_1111111
    temp_bb = bin & col1
    if temp_bb:
        temp_score += 200 * num_bin_ones(temp_bb)
    temp_bb = bin & cols2
    if temp_bb:
        temp_score += 120 * num_bin_ones(temp_bb)
    temp_bb = bin & cols3
    if temp_bb:
        temp_score += 70 * num_bin_ones(temp_bb)
    temp_bb = bin & cols4
    if temp_bb:
        temp_score += 40 * num_bin_ones(temp_bb)

    return temp_score


def feature_backup2(bitboards, player_index):
    player_bb = bitboards[player_index]
    adj_mask = bitboards[0] | bitboards[1] | 0b1_0111111_0111111_0000000_0000000_0000000_0000000_0000000_0000000_0000000
    bottom = 0b0000001_0000001_0000001_0000001_0000001_0000001_0000001
    final_score = 0
    score1 = np.inf
    score2 = 900_000
    score3 = 50_000
    if player_index:
        score1 *= -1
        score2 *= -1
        score3 *= -1

    # 3 stones

    # horizontal
    # free space on right and left side
    # we also check if one could immediately place a stone in both spaces
    if player_bb >> 7 & player_bb >> 14 & player_bb >> 21 & ~adj_mask & ~(adj_mask >> 28) & (
            adj_mask << 1 | bottom) & (adj_mask >> 27 | bottom >> 28):
        return score1
    else:
        # free space only on right
        temp_bb = player_bb & player_bb >> 7 & player_bb >> 14 & ~(adj_mask >> 21)
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)
        # free space only on the left
        else:
            temp_bb = ~adj_mask & player_bb >> 7 & player_bb >> 14 & player_bb >> 21
            if temp_bb:
                final_score += score2 * num_bin_ones(temp_bb)

    # 3 stones
    # horizontal
    temp_bb = (~(adj_mask & adj_mask >> 28) & ((adj_mask << 1 | bottom) & (adj_mask >> 27 | bottom >> 28))) & (
                player_bb >> 7 & player_bb >> 14 & player_bb >> 21)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 28):
            return score1
        final_score += score2 * num_bin_ones(temp_bb)

    # diagonal \
    temp_bb = (~(adj_mask & adj_mask >> 24) & (adj_mask << 1 & (adj_mask >> 23 | bottom >> 24))) & (
                player_bb >> 6 & player_bb >> 12 & player_bb >> 18)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 24):
            return score1
        final_score += score2 * num_bin_ones(temp_bb)

    # diagonal /
    temp_bb = (~(adj_mask & adj_mask >> 32) & ((adj_mask << 1 | bottom) & (adj_mask >> 31))) & (
                player_bb >> 8 & player_bb >> 16 & player_bb >> 24)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 32):
            return score1
        final_score += score2 * num_bin_ones(temp_bb)

    # vertical
    temp_bb = player_bb & (player_bb >> 1) & (player_bb >> 2)
    if temp_bb:
        final_score += score2 * num_bin_ones(temp_bb)



def feature_1backup(bitboards, player_index):
    player_bb = bitboards[player_index]
    adj_mask = bitboards[0] | bitboards[1] | 0b1_0111111_0111111_0000000_0000000_0000000_0000000_0000000_0000000_0000000
    bottom = 0b0000001_0000001_0000001_0000001_0000001_0000001_0000001
    score = np.inf
    if player_index:
        score *= -1

    # get 1s if (1 & 1) & 1
    # horizontal
    if (~(adj_mask | adj_mask >> 28) & ((adj_mask << 1 | bottom) & (adj_mask >> 27 | bottom >> 28))) & (player_bb >> 7 & player_bb >> 14 & player_bb >> 21):
        return score

    # diagonal \
    if (~(adj_mask | adj_mask >> 24) & (adj_mask << 1 & (adj_mask >> 23 | bottom >> 24))) & (player_bb >> 6 & player_bb >> 12 & player_bb >> 18):
        return score

    # diagonal /
    if (~(adj_mask | adj_mask >> 32) & ((adj_mask << 1 | bottom) & (adj_mask >> 31))) & (player_bb >> 8 & player_bb >> 16 & player_bb >> 24):
        return score

    return 0