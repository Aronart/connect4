# bitboards adapted from https://github.com/d
# enkspuren/BitboardC4/blob/master/BitboardDesign.md
import array as arr


class Game:

    def __init__(self, game_mode):
        # player 1
        self.p1 = None
        # player 2
        self.p2 = None
        rows_count = 6
        cols_count = 7
        # game board, contains 0, 1, or 2 entries
        self.board = arr.array("i", [[0 for x in range(cols_count)] for x in range(rows_count)])
        self.counter = 0
        self.moves = []
        self.game_mode = game_mode

    def run_game(self):
        if self.p1 is None or self.p2 is None:
            print("Player(s) not initialized")
            return
        while True:
            print("Turn ", self.counter)
            # player 1 always starts
            # player 1
            chosen_column = -1
            if self.counter & 1:
                chosen_column = self.p1.make_move(self.board, self.counter)
            # player 2
            else:
                chosen_column = self.p2.make_move(self.board, self.counter)
            self.counter += 1

            if not self.move_legal(chosen_column):
                print("The winner is ", self.get_player(self.counter ^ 1))



    def move_legal(self, column):
        return self.board[0][column] == 0

    def is_win(self):
        pass

    def get_last_player(self):
        return ["Player 1", "Player 2"][self.counter & 1]

    def get_player(self, player_index):
        return ["Player 1", "Player 2"][player_index]