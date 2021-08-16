from abc import ABCMeta, abstractmethod


class AI(metaclass=ABCMeta):
    @abstractmethod
    def make_move(self, board, counter):
        pass
