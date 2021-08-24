from Game import Game
from GameMode import GameMode
from Policy import Policy


def main():
    # print(num_bin_ones(51))
    game_mode = GameMode.MINMAX
    game = Game(game_mode)
    policy = Policy(game)

    policy.configure()
    game.run_game()


if __name__ == "__main__":
    main()
