from helpers import random_color, create_block_batch, check_collision, collision_animation
from screen import GameScreen
from block_manager import BlockManager
from player import Player

def test_random_color():
    """tests if tuple of correct lengths is returned and with not too bright colors"""
    new_color_tuple = random_color()
    assert isinstance(new_color_tuple, tuple)
    assert len(new_color_tuple) == 3
    red, green, blue = random_color()
    assert red < 220 or green < 220 or blue < 220


def test_create_block_batch():
    """
    - testing block batch feature for multiple cases; init classes to get default params for the function
        args:
    - "block_batch_min": int defining the bottom boundary of amount of blocks in one batch
    - "block_batch_max": int defining the upper boundary of amount of blocks in one batch
    - "block_batch_y_gap": min. space between every y-coordinates
    - "x_genesis": x-genesis-coordinate right beyond the visible screen where the blocks are generated
    - "screen": instance of GameScreen
    """
    screen = GameScreen()
    blocks = BlockManager(screen)
    # test with default values from BlockManager
    new_batch = create_block_batch(
        block_batch_min=blocks.block_batch_min,
        block_batch_max=blocks.block_batch_max,
        block_batch_y_gap=blocks.block_batch_y_gap,
        x_genesis=blocks.x_genesis_cor,
        screen=screen
    )
    assert isinstance(new_batch, list)
    assert 0 <= len(new_batch) <= 3
    # test with exactly one block generated for otherwise default values
    new_batch = create_block_batch(
        block_batch_min=1,
        block_batch_max=1,
        block_batch_y_gap=blocks.block_batch_y_gap,
        x_genesis=blocks.x_genesis_cor,
        screen=screen
    )
    assert len(new_batch) == 1
    # x-coordinate of result tuple: ; x_gen equals 320
    assert new_batch[0][0] == 320
    # y-coordinate of result tuple: screen.bottom_boundary=-240 + 12, screen.top_boundary=250 - 12
    assert -228 <= new_batch[0][1] <= 238


def test_check_collision():
    """
    check if collisions of player and blocks are detected for multiples cases
        args:
    - player object
    - block container with list of block objects
    returns:
    - true for collision with any block
    - otherwise false
    """
    screen = GameScreen()
    player = Player(screen)
    blocks = BlockManager(screen)
    # case 1: no collision if block container is empty
    blocks.block_container.clear()
    assert not check_collision(player, blocks.block_container)
    # case 2: render at least one block which doesn't collide with players default position (0, -265)
    blocks.render_blocks([(0, 0), (50, 100)])
    assert not check_collision(player, blocks.block_container)
    # case 3: render block directly at player default position to detect collision
    blocks.block_container.clear()
    blocks.render_blocks([(0, -265), (50, 100)])
    assert check_collision(player, blocks.block_container)
    # case 4: render block near player position to detect collision
    blocks.block_container.clear()
    player._turtle_player.goto(0, 0)
    blocks.render_blocks([(5, 5), (50, 100)])
    assert check_collision(player, blocks.block_container)


def test_collision_animation():
    """replaces player with an explosion effect for 0.5s"""
    screen = GameScreen()
    player = Player(screen)
    # check for correct player shape before collision animation
    assert player._turtle_player.shape() == "car.gif"
    # check for updated shape after collision executed
    collision_animation(player, screen)
    assert player._turtle_player.shape() == "explosion.gif"

