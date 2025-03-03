from helpers import random_color, create_block_batch, check_collision, collision_animation
from screen import GameScreen
from block_manager import BlockManager
from player import Player
import pytest


@pytest.mark.parametrize("i", range(5))
def test_random_color(i):
    """test parametrized 5 times if tuple of correct lengths is returned and with not too bright colors"""
    new_color_tuple = random_color()
    assert isinstance(new_color_tuple, tuple)
    assert len(new_color_tuple) == 3
    red, green, blue = random_color()
    assert red < 220 or green < 220 or blue < 220


@pytest.mark.parametrize(
    "block_batch_min, block_batch_max, block_batch_y_gap, x_genesis_cor",
    [
        (0, 3, 25, 320),
        (1, 1, 25, 320),
        (5, 5, 25, 320),
        (1, 10, 25, 320),
    ]
)
def test_create_block_batch_params(block_batch_min, block_batch_max, block_batch_y_gap, x_genesis_cor):
    """
    - parametrized testing block batch feature for multiple cases
    - function needs screen as only object input to calc top and bottom boundaries
    - testing if return value "a list of tuples with block coordinates for the batch" is correct
    """
    screen = GameScreen()
    batch = create_block_batch(
        block_batch_min=block_batch_min,
        block_batch_max=block_batch_max,
        block_batch_y_gap=block_batch_y_gap,
        x_genesis=x_genesis_cor,
        screen=screen
    )
    # basic checks
    assert isinstance(batch, list)
    assert block_batch_min <= len(batch) <= block_batch_max
    for (x_coord, y_coord) in batch:
        # all x-coordinates of result tuples must equal: x_gen = 320
        assert x_coord == x_genesis_cor
        # all y-coordinates must lie between screen.bottom_boundary=-240 + 12 and screen.top_boundary=250 - 12
        assert screen.bottom_boundary + 12 <= y_coord <= screen.top_boundary - 12
    # sort y-coordinates for y-gap check
    sorted_ys = sorted([y for (_, y) in batch])
    # check for y-gap overlapping
    for i in range(len(sorted_ys) - 1):
        assert abs(sorted_ys[i + 1] - sorted_ys[i]) >= block_batch_y_gap


@pytest.mark.parametrize(
    "player_x, player_y, block_x, block_y, expected_collision",
    [
        (0, 0, None, None, False),  # block container empty scenario
        (0, -265, 0, 0, False),
        (0, -265, 0, -265, True),   # direct hit scenario
        (0, 0, 5, 5, True),
        (10, 10, 15, 10, True),     # collision from the side
    ]
)
def test_check_collision_params(player_x, player_y, block_x, block_y, expected_collision):
    """
    - parametrized check if collisions of player and blocks are detected for multiples cases
    - none values for block x, block y to test case "block container is completely empty"
    """
    screen = GameScreen()
    blocks = BlockManager(screen)
    # clear block container for testing
    blocks.block_container.clear()
    # render block in needed format for not none values
    if block_x is not None and block_y is not None:
        blocks.render_blocks([(block_x, block_y)])
    # create player directly at certain position
    player = Player(screen, start_x=player_x, start_y=player_y)
    assert check_collision(player, blocks.block_container) == expected_collision


def test_collision_animation():
    """replaces player with an explosion effect for 0.5s"""
    screen = GameScreen()
    player = Player(screen)
    # check for correct player shape before collision animation
    assert player._turtle_player.shape() == "car.gif"
    # check for updated shape after collision executed
    collision_animation(player, screen)
    assert player._turtle_player.shape() == "explosion.gif"
