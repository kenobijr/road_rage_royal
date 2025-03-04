from src.screen import GameScreen
from src.block_manager import Block, BlockManager
import pytest


def test_Block_init_turtle():
    """
    - testing the attributes of the internal turtle object when initiating a new block
    - omit testing height and width attributes since doing it via the respective getter methods
    """
    block = Block(x=0, y=0)
    assert hasattr(block, "_turtle")
    assert block._turtle.shape() == "square"
    assert not block._turtle.isdown()
    assert block._turtle.pos() == (0.0, 0.0)


@pytest.mark.parametrize(
    "initial_x, initial_y, move_distance, expected_x, expected_y",
    [
        (0, 0, 5, -5, 0),
        (100, 50, 10, 90, 50),
        (20, 20, 20, 0, 20)
    ]
)
def test_Block_move_params(initial_x, initial_y, move_distance, expected_x, expected_y):
    """parametrized test to move a single block one time for multiple starting positions"""
    block = Block(x=initial_x, y=initial_y)
    block.move(move_distance)
    assert block._turtle.pos() == (expected_x, expected_y)


@pytest.mark.parametrize(
    "initial_x, initial_y, expected_result",
    [
        (0, 0, False),
        (-320, 0, False),
        (150, 50, False),
        (-321, 0, True),
        (-400, -50, True)
    ]
)
def test_Block_off_screen_params(initial_x, initial_y, expected_result):
    """parametrized test if block is off the screen for multiple start positions and same x-wrecking-coordinate"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    block = Block(initial_x, initial_y)
    assert block.is_off_screen(blocks.x_wrecking_cor) == expected_result


def test_Block_getters():
    """test getters delivering data about block turtle state to outside callers"""
    block = Block(x=0, y=0)
    assert block.get_ycor() == block._turtle.ycor()
    assert block.get_xcor() == block._turtle.xcor()
    # width and height values precalculated due to construction with stretch size
    assert block.get_width == 40
    assert block.get_height == 20


def test_BlockManager_init_attributes():
    """test default values for BlockManager on initialization"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    assert hasattr(blocks, "block_container")
    assert blocks.speed == 0.2
    assert blocks.distance == 5
    assert blocks.block_batch_max == 3
    assert blocks.block_batch_min == 0
    assert blocks.block_batch_x_gap == 80
    assert blocks.block_batch_y_gap == 25
    assert blocks.x_genesis_cor == 320
    assert blocks.x_wrecking_cor == -320


def test_BlockManager_add_blocks():
    """
    test add_blocks method (on default 0-3 added) for following cases:
    1. block container is empty
    2. block container is not empty and no additional blocks have to be generated
    3. block container is not empty and additional blocks have to be generated
    """
    screen = GameScreen()
    blocks = BlockManager(screen)
    # case 1: empty block container list; block container can contain 0-3 block objects
    blocks.block_container.clear()
    blocks.add_blocks()
    assert 0 <= len(blocks.block_container) <= 3
    # case 2: empty block container and add one block object with x-coordinate preventing more blocks to be generated
    blocks.block_container.clear()
    blocks.render_blocks([(240, 0)])
    blocks.add_blocks()
    assert len(blocks.block_container) == 1
    # case 3: empty block container and add one block object with x-coordinate in which case more blocks are generated
    blocks.block_container.clear()
    blocks.render_blocks([(239, 0)])
    blocks.add_blocks()
    assert 1 <= len(blocks.block_container) <= 4


def test_BlockManager_render_blocks():
    """test render block method; with missing argument and with 2 blocks to render"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    blocks.block_container.clear()
    # test with missing argument
    with pytest.raises(TypeError):
        blocks.render_blocks()
    # test with 2 blocks to render
    blocks.render_blocks([(0, 0), (50, 100)])
    assert len(blocks.block_container) == 2
    assert blocks.block_container[0]._turtle.shape() == "square"
    assert blocks.block_container[0].get_xcor() == 0.0
    assert blocks.block_container[0].get_ycor() == 0.0
    assert blocks.block_container[1].get_xcor() == 50.0
    assert blocks.block_container[1].get_ycor() == 100.0
    assert not blocks.block_container[1]._turtle.isdown()


def test_BlockManager_move_blocks():
    """test move blocks method"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    # empty block container and add 2 block objects for testing
    blocks.block_container.clear()
    blocks.render_blocks([(0, 0), (50, 100)])
    blocks.move_blocks()
    assert blocks.block_container[0].get_xcor() == -5.0
    assert blocks.block_container[0].get_ycor() == 0.0
    assert blocks.block_container[1].get_xcor() == 45.0
    assert blocks.block_container[1].get_ycor() == 100.0


def test_BlockManager_wreck_blocks():
    """test wreck block for cases: no block is wrecked; at least one block is wrecked"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    blocks.block_container.clear()
    # case 1: no block is wrecked; x_wrecking coordinate equals -320
    blocks.render_blocks([(-320, 0), (50, 100)])
    blocks.wreck_blocks()
    assert len(blocks.block_container) == 2
    # case 2: first block is wrecked; second still exists
    blocks.block_container.clear()
    blocks.render_blocks([(-321, 0), (50, 100)])
    blocks.wreck_blocks()
    assert len(blocks.block_container) == 1
    assert blocks.block_container[0].get_xcor() == 50.0


def test_BlockManager_reset():
    """test reset function after collision and player wants to play further game"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    # increase game difficulty (with high level 7 as param) to check if all values are reset to default
    blocks.increase_difficulty(7)
    blocks.reset()
    assert len(blocks.block_container) == 0
    assert blocks.block_batch_max == 3
    assert blocks.block_batch_min == 0
    assert blocks.speed == 0.2


@pytest.mark.parametrize(
    "level, expected_speed, expected_batch_min, expected_batch_max, expected_batch_x_gap, expected_batch_y_gap",
    [
        (2, 0.19, 0, 3, 80, 25),
        (4, 0.19, 0, 4, 80, 25),
        (5, 0.19, 0, 4, 76, 23.75),
        (77, 0.19, 1, 4, 76, 23.75),
    ]
)
def test_BlockManager_increase_difficulty_params(
    level,
    expected_speed,
    expected_batch_min,
    expected_batch_max,
    expected_batch_x_gap,
    expected_batch_y_gap
):
    """
    parameterized test increasing difficulty for 4 cases depending on the level delivered as param:
    case 1: level 1-2
    case 2: level 3-4
    case 3: level 5-6
    case 4: level >=7
    """
    screen = GameScreen()
    blocks = BlockManager(screen)
    blocks.increase_difficulty(level)
    assert blocks.speed == expected_speed
    assert blocks.block_batch_min == expected_batch_min
    assert blocks.block_batch_max == expected_batch_max
    assert blocks.block_batch_x_gap == expected_batch_x_gap
    assert blocks.block_batch_y_gap == expected_batch_y_gap
