import numpy as np


class Game:

    def __init__(self, game_mode):
        # player 1
        self.p1 = None
        # player 2
        self.p2 = None
        rows_count = 6
        cols_count = 7
        # game board, contains 0, 1, or 2 entries
        self.board = np.array("i", [[0 for x in range(cols_count)] for x in range(rows_count)])
        self.counter = 0
        self.moves = []
        self.game_mode = game_mode

    def run_game(self):
        if self.p1 is None or self.p2 is None:
            print("Player(s) not initialized.")
            return
        while True:
            print(f"Turn {self.counter}:")
            # player 1 always starts
            # player 1
            if self.counter & 1:
                chosen_column = self.p1.make_move(self.board, self.counter)
            # player 2
            else:
                chosen_column = self.p2.make_move(self.board, self.counter)

            self.moves.append(chosen_column)

            if not self.is_legal_move(chosen_column):
                print(f"The winner is {self.get_player(self.counter ^ 1)}. {self.get_current_player()} made an "
                      f"illegal move.")
                return

            self.insert_move(chosen_column)

            if self.is_win():
                print(f"{self.get_current_player()} is the winner.")
                return

            if self.is_full_board():
                print("No winner. Game board is full.")
                return

            self.counter += 1

    def is_legal_move(self, column):
        return self.board[0][column] == 0

    def is_win(self):
        # there cannot be a win before the 7th stone is placed
        if self.counter < 6:
            return False
        player_stone = self.get_current_stone()
        rows = 6
        cols = 7
        for x in range(rows):
            for y in range(cols):
                if self.board[x][y] == player_stone:
                    # horizontal
                    if y <= 3 and self.board[x][y + 1] == player_stone and self.board[x][y + 2] == player_stone and \
                            self.board[x][y + 3] == player_stone:
                        return True
                    # vertical
                    if x <= 2 and self.board[x + 1][y] == player_stone and self.board[x + 2][y] == player_stone and \
                            self.board[x + 3][y] == player_stone:
                        return True
                    # / diagonal
                    if x <= 2 and y >= 3 and self.board[x + 1][y - 1] == player_stone and self.board[x + 2][
                        y - 2] == player_stone and self.board[x + 3][y - 3] == player_stone:
                        return True
                    # \ diagonal
                    if x <= 2 and y <= 3 and self.board[x + 1][y + 1] == player_stone and self.board[x + 2][
                        y + 2] == player_stone and self.board[x + 3][y + 3] == player_stone:
                        return True
        return False

    def is_full_board(self):
        cols = 7
        for y in range(cols):
            if self.board[0][y] == 0:
                return False
        return True

    def insert_move(self, column):
        for x in range(5, -1, -1):
            if self.board[x][column] == 0:
                self.board[x][column] = self.get_current_stone()

    def get_current_player(self):
        return ["Player 1", "Player 2"][self.counter & 1]

    def get_player(self, player_index):
        return ["Player 1", "Player 2"][player_index]

    def get_current_stone(self):
        return [1, 2][self.counter & 1]
