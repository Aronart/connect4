from GameMode import GameMode
from MinMaxAI import MinMaxAI
from RandomAI import RandomAI


class Policy:
    def __init__(self, context):
        self.context = context

    def configure(self):
        if self.context.game_mode == GameMode.MINMAX:
            self.context.p1 = MinMaxAI()
            self.context.p2 = MinMaxAI()
        elif self.context.game_mode == GameMode.RANDOM:
            self.context.p1 = RandomAI()
            self.context.p2 = RandomAI()
        elif self.context.game_mode == GameMode.MINMAX_VS_RANDOM:
            self.context.p1 = MinMaxAI()
            self.context.p2 = RandomAI()
        elif self.context.game_mode == GameMode.RANDOM_VS_MINMAX:
            self.context.p1 = RandomAI()
            self.context.p2 = MinMaxAI()
