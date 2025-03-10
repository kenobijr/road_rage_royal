from src.screen import GameScreen
from src.player import Player
from random import randint, sample
from typing import List, Tuple
import time
# needed for fine-tuning for collision detection function (visible crash)
OVERLAP_MARGIN: int = 2


def random_color() -> Tuple[int, int, int]:
    """
    - generates a random RGB color tuple of not too bright colors on the white background
    - returns:
        Tuple[int, int, int]: a tuple of three integers representing RGB values
    """
    while True:
        r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
        if r < 220 or g < 220 or b < 220:
            return r, g, b


def create_block_batch(
        block_batch_min: int,
        block_batch_max: int,
        block_batch_y_gap: float,
        x_genesis: int,
        screen: GameScreen
) -> List[Tuple[int, int]]:
    """
    generate a list of tuples with random y-coordinates & constant x-genesis coordinate for a block batch ensuring that:
        1. there are no duplicate y-coordinates
        2. the y-coordinates are spaced apart to prevent overlapping
        3. the amount of blocks per batch is a randint between block_batch_min and block_batch_max
        4. every single y-coordinate is randomly generated along the y-axis between bottom and top screen
    args:
    - "block_batch_min": int defining the bottom boundary of amount of blocks in one batch
    - "block_batch_max": int defining the upper boundary of amount of blocks in one batch
    - "block_batch_y_gap": min. space between every y-coordinates
    - "x_genesis": x-genesis-coordinate right beyond the visible screen where the blocks are generated
    - "screen": instance of GameScreen
    return:
    - a list of tuples with block coordinates for the batch
    """
    # define the amount of blocks to be generated for the batch randomly within the range
    amount_blocks: int = randint(block_batch_min, block_batch_max)
    # create list of all possible y coordinates
    possible_y_coordinates = list(range(screen.bottom_boundary + 12, screen.top_boundary - 12, int(block_batch_y_gap)))
    # Randomly sample the required amount; ensure no more samples are drawn than possible y-coordinates
    block_batch_y_coordinates = sample(possible_y_coordinates, min(amount_blocks, len(possible_y_coordinates)))
    # using the y-coordinates create the tuples with constant x-genesis-coordinate
    return [(x_genesis, y_cor) for y_cor in block_batch_y_coordinates]


def check_collision(player: Player, block_container) -> bool:
    """
    - bounding box collision detection to check if any of the blocks collides with the player
    - overlapping margin added to ensure the rectangles are close to each other visibly at collisions
    args:
    - player object
    - block container with list of block objects
    returns:
    - true for collision with any block
    - otherwise false
    """
    # calc player boundary with coordinates at center + / - width / height + / - overlap margin
    player_right: float = player.get_xcor() + (player.get_width() / 2) - OVERLAP_MARGIN
    player_left: float = player.get_xcor() - (player.get_width() / 2) + OVERLAP_MARGIN
    player_top: float = player.get_ycor() + (player.get_height() / 2) - OVERLAP_MARGIN
    player_bottom: float = player.get_ycor() - (player.get_height() / 2) + OVERLAP_MARGIN
    # check for collision of player box with all existing blocks on the screen
    for block in block_container:
        block_right: float = block.get_xcor() + (block.get_width / 2)
        block_left: float = block.get_xcor() - (block.get_width / 2)
        block_top: float = block.get_ycor() + (block.get_height / 2)
        block_bottom: float = block.get_ycor() - (block.get_height / 2)
        if (
            player_right > block_left and
            player_left < block_right and
            player_top > block_bottom and
            player_bottom < block_top
        ):
            return True
    return False


def collision_animation(player: Player, screen: GameScreen) -> None:
    """replaces player with an explosion effect for 0.5s"""
    player.update_shape("assets/explosion.gif")
    screen.update_screen()
    time.sleep(1)
