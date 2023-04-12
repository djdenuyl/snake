"""
Game coordinates

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-04-12
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int

    @property
    def xy(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def yx(self):
        return self.y, self.x

    def __sub__(self, other) -> Coord:
        if self.__class__ == other.__class__:
            xy = [z[0] - z[1] for z in zip(self.xy, other.xy)]
            return Coord(*xy)

        raise NotImplemented

    def __add__(self, other) -> Coord:
        if self.__class__ == other.__class__:
            xy = [z[0] + z[1] for z in zip(self.xy, other.xy)]
            return Coord(*xy)

        raise NotImplemented

    def __hash__(self) -> int:
        return hash(self.xy)
