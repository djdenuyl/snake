from dataclasses import dataclass, field
from snake.direction import Direction
from snake.coord import Coord
from typing import Union


@dataclass
class Snake:
    direction: Direction = Direction.LEFT
    length: int = 3
    head: Union[Coord, tuple[int, int]] = Coord(5, 5)
    segments: list[Coord] = field(default_factory=list, repr=False)

    def __post_init__(self):
        if isinstance(self.head, tuple):
            self.head = Coord(*self.head)

        self._init_segments()

    def _init_segments(self):
        for i in range(self.length):
            if i == 0:
                self.segments.append(self.head)
            else:
                self.segments.append(self.segments[-1] - self.direction.value)

    def move(self, has_fruit: bool = False):
        """ move one place """
        self.segments.insert(0, self.head + self.direction.value)

        # if the snake didn't catch the fruit, pop the last element from the segments
        if not has_fruit:
            self.segments.pop(-1)

        self.head = self.segments[0]
