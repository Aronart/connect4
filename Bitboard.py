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


def num_bin_ones(bin):
    num = 0
    while(bin):
        num += 1
        bin &= bin - 1
    return num


def feature_score(bitboards, player_index):
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
    temp_bb = (~(adj_mask & adj_mask >> 28) & ((adj_mask << 1 | bottom) & (adj_mask >> 27 | bottom >> 28))) & (player_bb >> 7 & player_bb >> 14 & player_bb >> 21)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 28):
            return score1
        final_score += score2 * num_bin_ones(temp_bb)


    # diagonal \
    temp_bb = (~(adj_mask & adj_mask >> 24) & (adj_mask << 1 & (adj_mask >> 23 | bottom >> 24))) & (player_bb >> 6 & player_bb >> 12 & player_bb >> 18)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 24):
            return score1
        final_score += score2 * num_bin_ones(temp_bb)

    # diagonal /
    temp_bb = (~(adj_mask & adj_mask >> 32) & ((adj_mask << 1 | bottom) & (adj_mask >> 31))) & (player_bb >> 8 & player_bb >> 16 & player_bb >> 24)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 32):
            return score1
        final_score += score2 * num_bin_ones(temp_bb)

    # vertical
    temp_bb = player_bb & (player_bb >> 1) & (player_bb >> 2)
    if temp_bb:
        final_score += score2 * num_bin_ones(temp_bb)

    # not checking if you also can immediately put a stone in the empty space
    directions = [1, 7, 6, 8]
    for direction in directions:
        temp_bb = player_bb & ~(adj_mask >> direction) & (player_bb >> (2 * direction)) & (player_bb >> (3 * direction))
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)
        temp_bb = player_bb & (player_bb >> direction) & ~(adj_mask >> (2 * direction)) & (player_bb >> (3 * direction))
        if temp_bb:
            final_score += score2 * num_bin_ones(temp_bb)

    # 2 stones
    # not checking if you also can immediately put a stone in the empty spaces
    # horizontal
    temp_bb = ~(adj_mask & adj_mask >> 21) & (
                player_bb >> 7 & player_bb >> 14)
    if temp_bb:
        if temp_bb & ~(adj_mask | adj_mask >> 21):
            final_score += score3 * num_bin_ones(temp_bb)
        else:
            # empty on left
            if ~adj_mask & temp_bb:
                pass
            # empty on right
            else:
                pass

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



    return final_score



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