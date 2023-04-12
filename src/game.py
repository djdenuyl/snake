"""
Snake game logic

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-04-12
"""
from __future__ import annotations
from random import choice
from numpy import zeros, array, where, column_stack
from src.coord import Coord
from src.direction import Direction, opposite
from src.fruit import Fruit
from src.snake import Snake


class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.shape = self.width, self.height

        self.snake = Snake(length=3, direction=Direction.LEFT)
        self.fruit = self.place_fruit()

    def new(self) -> array:
        """ create a new empty canvas """
        return zeros(self.shape)

    def draw(self, board: array) -> array:
        """ draw the snake on the board """
        segments = self.snake.segments

        # check and correct if segments are out of bounds of the canvas
        for s in segments:
            if s.x < 0:
                s.x += self.width
            if s.x > self.width - 1:
                s.x -= self.width
            if s.y < 0:
                s.y += self.height
            if s.y > self.height - 1:
                s.y -= self.height

        self.snake.head = segments[0]

        # draw the head on the board
        board[self.snake.head.yx] = 2

        # draw the body on the board
        for s in segments[1:]:
            board[s.yx] = 1

        # draw the fruit on the board
        board[self.fruit.location.yx] = 3

        return board

    def next(self) -> array:
        """ create next game frame """
        # start with an empty canvas
        board = self.new()

        # move the snake
        if self.is_snake_colliding_with_fruit():
            self.snake.move(has_fruit=True)
            self.fruit = self.place_fruit()
        else:
            self.snake.move()

        # draw the snake on the board
        self.draw(board)

        return board

    def change_snake_direction(self, direction: Direction):
        """ change the snake direction if allowed """
        if direction != opposite(self.snake.direction):
            self.snake.direction = direction

    def is_snake_colliding_with_self(self) -> bool:
        if self.snake.head in self.snake.segments[1:]:
            return True

        return False

    def is_snake_colliding_with_fruit(self) -> bool:
        if self.snake.head == self.fruit.location:
            return True

        return False

    def place_fruit(self) -> Fruit:
        board_coords = set(Coord(*i) for i in column_stack(where(self.new() == 0)).tolist())
        snake_coords = {s for s in self.snake.segments}

        # the options to place a fruit are all places where the snake is not
        options = board_coords ^ snake_coords

        return Fruit(location=choice(list(options)))


if __name__ == '__main__':
    self = Game(10, 10)
