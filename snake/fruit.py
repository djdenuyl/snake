from dataclasses import dataclass
from snake.coord import Coord
from typing import Union


@dataclass
class Fruit:
    location: Union[Coord, tuple[int, int]]

    def __post_init__(self):
        if isinstance(self.location, tuple):
            self.location = Coord(*self.location)
