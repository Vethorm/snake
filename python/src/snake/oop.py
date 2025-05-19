from enum import StrEnum
from random import randint

from typing import Self
import argparse


class Direction(StrEnum):
    UP: str = "w"
    DOWN: str = "s"
    LEFT: str = "a"
    RIGHT: str = "d"


class GameOption(StrEnum):
    QUIT: str = "quit"


class GameInput:
    """Class to validate or check inputs"""

    @staticmethod
    def is_direction(s: str) -> bool:
        return s in [d.value for d in Direction]

    @staticmethod
    def is_game_option(s: str) -> bool:
        return s in [o.value for o in GameOption]

    @staticmethod
    def is_valid(s: str) -> bool:
        return GameInput.is_direction(s) or GameInput.is_game_option(s)


class InputHandler:
    """Handle user inputs and validate"""

    def get_user_input(self) -> str:
        """Get user input from the console"""
        return input("Enter direction (w/a/s/d/quit):").lower()

    def process_user_input(self) -> tuple[bool, Direction | None]:
        """Get user input and validate it

        When inputs are invalid we keep asking for input
        """
        while True:
            user_input = self.get_user_input()

            if GameInput.is_valid(user_input):
                if GameInput.is_direction(user_input):
                    return True, Direction(user_input)
                else:
                    return False, None


class BoardObjects:
    EMPTY = " "
    FOOD = "o"
    SNAKE = "S"


class Location:
    """Represents a location at a height and a width"""

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def new_location_from_direction(self, direction: Direction) -> Self:
        """Generates a new location based on the given direction"""
        if direction == Direction.UP:
            return Location(self.height - 1, self.width)
        if direction == Direction.DOWN:
            return Location(self.height + 1, self.width)
        if direction == Direction.LEFT:
            return Location(self.height, self.width - 1)
        if direction == Direction.RIGHT:
            return Location(self.height, self.width + 1)

    def __eq__(self, value: Self):
        if not isinstance(value, Location):
            return False
        return self.height == value.height and self.width == value.width


class Snake:
    """Represents a snake
    The snake is a list of locations, the locations are locations of the body
    The head of the snake is always the beginning
    """

    def __init__(self, height: int, width: int):
        self.snake: list[Location] = [Location(height, width)]

    def head(self) -> Location:
        return self.snake[0]

    def update_snake(self, location: Location, grow_snake: bool) -> None:
        """Update the snake head to a new location

        If grow snake is passed the tail location is kept"""
        self.snake.insert(0, location)
        if not grow_snake:
            self.snake.pop()

    def is_part_of_snake(self, location: Location) -> bool:
        """Checks to see if the location is part of the snake"""
        return location in self.snake


class SnakeGame:
    """Class that represents the game and game operations"""

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.food: Location = None
        self.snake: Snake = None
        self.score = 0
        self.initialize()
        print(
            f"Board initialized: food({self.food.height, self.food.width}), snake({self.snake.head().height, self.snake.head().width})"
        )

    def invalid_location(self, location: Location) -> bool:
        """Checks to see if a location is invalid

        Invalid locations are outside of the board or part of the snakes body
        """
        invalid_height = location.height >= self.height or location.height < 0
        invalid_width = location.width >= self.width or location.width < 0
        is_snake = self.snake.is_part_of_snake(location)
        return invalid_height or invalid_width or is_snake

    def update_game(self, direction: Direction) -> bool:
        """Updates the state of the game

        Given the direction we update the head of the snake

        If the head of the snake is a food location we grow the snake

        If the head of the snake is updated to an invalid location we return False, indicating the game is over
        """
        snake_head = self.snake.head()
        new_head = snake_head.new_location_from_direction(direction)

        if self.invalid_location(new_head):
            return False
        else:
            food_consumed = self.food == new_head
            self.snake.update_snake(new_head, grow_snake=food_consumed)
            if food_consumed:
                self.score += 1
                self.food = self.random_location()
            return True

    def initialize(self):
        """Initialize the game with food and a snake"""
        food_location = self.random_location()
        self.food = Location(food_location.height, food_location.width)
        snake_start_location = self.random_location()
        self.snake = Snake(snake_start_location.height, snake_start_location.width)

    def print_board(self):
        """Print the game board with triple-width cells"""
        print("=== Game State ===")

        print("+" + "---+" * self.width)

        for height in range(self.height):
            row = []
            for width in range(self.width):
                location = Location(height, width)
                tile = BoardObjects.EMPTY
                if self.food == location:
                    tile = BoardObjects.FOOD
                if self.snake.is_part_of_snake(location):
                    tile = BoardObjects.SNAKE
                row.append(" " + tile + " ")

            print("|" + "|".join(row) + "|")
            print("+" + "---+" * self.width)

    def random_location(self) -> Location:
        """Generate a random location on an empty tile"""
        while True:
            location = Location(randint(0, self.height - 1), randint(0, self.width - 1))
            not_food = self.food != location
            not_snake = self.snake is None or not self.snake.is_part_of_snake(location)
            if not_food and not_snake:
                return location


def run_game():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--height", default=5, type=int, help="Height of the board", required=False
    )
    parser.add_argument(
        "--width", default=5, type=int, help="Width of the board", required=False
    )

    args = parser.parse_args()
    game = SnakeGame(args.height, args.width)
    input_handler = InputHandler()

    while True:
        game.print_board()
        continue_game, direction = input_handler.process_user_input()
        if continue_game:
            game_in_progress = game.update_game(direction)
            if not game_in_progress:
                print("GAME OVER!")
                print(f"Score: {game.score}")
                break


run_game()
