from GameMode import GameMode
from MinMaxAI import MinMaxAI


class Policy:
    def __init__(self, context):
        self.context = context

    def configure(self):
        if self.context.gameMode == GameMode.MINMAX:
            self.context.p1 = MinMaxAI()
            self.context.p2 = MinMaxAI()
