from pprint import pprint
from random import randint
import argparse

# board should be an M x N board where the game will be played
M = 5  # height
N = 3  # width

# constants
EMPTY = " "
FOOD = "o"
SNAKE_BODY = "S"

# directions
UP = "W"
DOWN = "S"
LEFT = "A"
RIGHT = "D"

QUIT = "QUIT"

# board
board = []


# snake
snake = []

# food
food = None

# points
points = 0


# functions
def generate_board():
    """Generate the board"""
    for _ in range(M):
        new_row = []
        for _ in range(N):
            new_row.append(EMPTY)
        board.append(new_row)


def is_width_invalid(w: int) -> bool:
    """Checks if the width value is on the board"""
    too_far_left = w < 0
    too_far_right = w > N - 1
    return too_far_left or too_far_right


def is_height_invalid(h: int) -> bool:
    """Checks if the height value is on the board"""
    too_far_left = h < 0
    too_far_right = h > M - 1
    return too_far_left or too_far_right


def is_snake_body(h, w) -> bool:
    """Checks if the location is part of the snake body"""
    condition = board[h][w] == SNAKE_BODY
    return condition


def is_not_valid(h, w) -> bool:
    """Checks if a location is valid
    
    Invalid locations are outside the board or on the snake body
    """
    is_invalid = is_width_invalid(w) or is_height_invalid(h) or is_snake_body(h, w)
    return is_invalid


def place_food() -> bool:
    """Places food at a location

    if the coordinates are on an invalid location we will return False

    Returns:
        (bool) whether or not the food was placed
    """
    global food
    h, w = random_board_location()
    while is_not_valid(h, w):
        h, w = random_board_location()
    else:
        board[h][w] = FOOD
        food = (h, w)
        return True


def new_snake() -> tuple[int, int] | None:
    """Places a new snake at a random location on the board"""
    h, w = random_board_location()
    while is_not_valid(h, w):
        h, w = random_board_location()

    board[h][w] = SNAKE_BODY
    new_head = (h, w)
    snake.insert(0, new_head)
    return new_head


def get_new_head(direction: str) -> tuple[int, int]:
    """Creates the new head location of the snake based on the direction"""
    head: tuple[int, int] = snake[0]

    if direction == UP:
        return (head[0] - 1, head[1])

    if direction == DOWN:
        return (head[0] + 1, head[1])

    if direction == LEFT:
        return (head[0], head[1] - 1)

    if direction == RIGHT:
        return (head[0], head[1] + 1)


def is_food(h, w) -> bool:
    """Checks to see if the location is food"""
    return food == (h, w)


def move_snake(direction: str) -> bool:
    """Moves the snake in the given direction
    
    If the snake is moved onto food the snake grows by size 1
    If the snake is moved into an invalid location, the snake isn't moved and we return false
    """
    global food
    global points

    h, w = get_new_head(direction)
    if is_not_valid(h, w):
        return False
    else:
        snake.insert(0, (h, w))
        board[h][w] = SNAKE_BODY

        if not is_food(h, w):
            # move tail
            tail_h, tail_w = snake.pop()
            board[tail_h][tail_w] = EMPTY
        else:
            food = None
            points += 1
        return True


def random_board_location() -> tuple[int, int]:
    """Generates a random board location"""
    return (randint(0, M - 1), randint(0, N - 1))


def valid_input(s: str) -> bool:
    """Validated our inputs"""
    return s in [UP, DOWN, RIGHT, LEFT, QUIT]


def get_input() -> str:
    """Prompts the user for input until a valid command is given"""
    while True:
        direction = input("Which direction (W/A/S/D/QUIT): ").upper()
        if valid_input(direction):
            break
        else:
            print('Invalid input!')
    return direction


def setup_board():
    """Setups up the board for a new turn
    
    If there is no food on the board generate new food
    If there is no snake on the board generate a new snake
    """
    if not food:
        place_food()
    if not snake:
        new_snake()


def main():
    generate_board()
    while True:
        # setup board for turn
        setup_board()

        # visualize board to user
        print("\n=== GAME STATE ===")
        pprint(board)

        # get user input
        direction = get_input()
        if direction == QUIT:
            break

        # execute user input
        successful = move_snake(direction)
        if not successful:
            print("Move invalid!")
            break

    print(">>> Game over")
    print(f">>> Score: {points}")

def run_game():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--height", default=5, type=int, help="Height of the board", required=False
    )
    parser.add_argument(
        "--width", default=5, type=int, help="Width of the board", required=False
    )

    args = parser.parse_args()

    global M, N
    M = args.height
    N = args.width

    main()


if __name__ == "__main__":
    run_game()
