from enum import Enum
from snake.coord import Coord


class Direction(Enum):
    UP = Coord(0, -1)
    DOWN = Coord(0, 1)
    LEFT = Coord(-1, 0)
    RIGHT = Coord(1, 0)


_OPPOSITE_DIRECTION_MAPPER = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}


def opposite(direction: Direction) -> Direction:
    """ return the opposite direction of the given direction """
    return _OPPOSITE_DIRECTION_MAPPER.get(direction)
