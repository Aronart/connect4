import array as arr
import AI


class MinMaxAI(AI):
    def __init__(self):
        # int in Python3 is equivalent to long in Python2
        self.bitboards = arr.array("i", [0, 0])
        self.height = arr.array("i", [0, 7, 15, 24, 30, 35, 42])

    def make_move(self, board, counter):
        self.bitboards[0], self.bitboards[1] = self.generate_bitboards(board)

    @staticmethod
    def generate_bitboards(board):
        bitboard1, bitboard2 = '', ''
        # Start with right-most column
        for j in range(6, -1, -1):
            # Add 0-bits to sentinel
            bitboard1 += '0'
            bitboard2 += '0'
            # Start with bottom row
            for i in range(0, 6):
                bitboard1 += ['0', '1'][board[i, j] == 1]
                bitboard2 += ['0', '1'][board[i, j] == 2]
        return int(bitboard1, 2), int(bitboard2, 2)
