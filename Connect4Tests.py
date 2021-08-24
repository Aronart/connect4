import unittest

from Bitboard import *


class Connect4Tests(unittest.TestCase):

    def test_process_board(self):
        cols_count = 7
        rows_count = 6
        board = np.array([[0 for x in range(cols_count)] for x in range(rows_count)])

        bitboards = np.array([0, 0], dtype=np.int64)
        bitboards[0], bitboards[1], height = process_board(board)

        make_move(bitboards, height, 0, 3)
        make_move(bitboards, height, 1, 4)

        make_move(bitboards, height, 0, 3)
        make_move(bitboards, height, 1, 3)

        make_move(bitboards, height, 0, 4)
        make_move(bitboards, height, 1, 2)

        self.assertEqual(bitboards[0], 0b0000000_0000000_0000010_0000011_0000000_0000000_0000000,
                         "Bitboard of player1 not as expected.")
        self.assertEqual(bitboards[1], 0b0000000_0000000_0000001_0000100_0000001_0000000_0000000,
                         "Bitboard of player2 not as expected.")

    def test_feature_score1(self):
        bitboards = np.array([0, 0], dtype=np.int64)

        bitboards[0] = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000000
        score = feature_score(bitboards, 0)
        self.assertEqual(score, 0)

        bitboards[0] = 0b0000000_0000000_0000000_0000001_0000000_0000000_0000000
        score = feature_score(bitboards, 0)
        self.assertEqual(score, 200)

        bitboards[0] = 0b0000000_0000000_0000000_0000000_0000001_0000000_0000000
        score = feature_score(bitboards, 0)
        self.assertEqual(score, 120)

        bitboards[0] = 0b0000000_0000001_0000000_0000000_0000000_0000001_0000000
        score = feature_score(bitboards, 0)
        self.assertEqual(score, 2*70)

        bitboards[0] = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000001
        score = feature_score(bitboards, 0)
        self.assertEqual(score, 40)

if __name__ == '__main__':
    unittest.main()
