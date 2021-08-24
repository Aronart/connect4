from enum import Enum


class GameMode(Enum):
    MINMAX = 1
    RANDOM = 2
    MINMAX_VS_RANDOM = 3
    RANDOM_VS_MINMAX = 4
