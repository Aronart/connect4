from abc import ABCMeta, abstractmethod
from numpy import numpy as np


class AI(metaclass=ABCMeta):
    @abstractmethod
    def find_move(self, board: np.array, counter: int) -> int:
        pass
