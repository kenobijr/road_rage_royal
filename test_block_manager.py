from screen import GameScreen
from block_manager import Block, BlockManager
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


def test_Block_move():
    """test the moving function to move a single block one time"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    block = Block(x=0, y=0)
    # move it one time by the distance saved in BlockManager
    block.move(blocks.distance)
    assert block._turtle.pos() == (-5.0, 0.0)


def test_Block_off_screen():
    """test if block is off the screen for a given x-wrecking-coordinate: """
    screen = GameScreen()
    blocks = BlockManager(screen)
    block = Block(x=0, y=0)
    # test if False is returned for on screen block with x-wrecking-coordinate saved in BlockManager
    assert not block.is_off_screen(blocks.x_wrecking_cor)
    # test exactly on the border
    block._turtle.goto(-320, 0)
    assert not block.is_off_screen(blocks.x_wrecking_cor)
    # test if True for off_screen
    block._turtle.goto(-321, 0)
    assert block.is_off_screen(blocks.x_wrecking_cor)


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
    test add_blocks method for following cases:
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
    # create one block: border is 240: 320 x_genesis_cor - 80 block_batch_x_gap
    blocks.render_blocks([(240, 0)])
    blocks.add_blocks()
    assert len(blocks.block_container) == 1
    # case 3: empty block container and add one block object with x-coordinate in which case more blocks are generated
    blocks.block_container.clear()
    blocks.render_blocks([(239, 0)])
    blocks.add_blocks()
    assert 1 <= len(blocks.block_container) <= 4


def test_BlockManager_render_blocks():
    """test render block method"""
    screen = GameScreen()
    blocks = BlockManager(screen)
    blocks.block_container.clear()
    # test with missing argument
    with pytest.raises(TypeError):
        blocks.render_blocks()
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


def test_BlockManager_increase_difficulty():
    """
    test increasing of difficulty for 4 cases depending on the level delivered as param:
    case 1: level 1-2
    case 2: level 3-4
    case 3: level 5-6
    case 4: level >=7
    """
    screen = GameScreen()
    blocks = BlockManager(screen)
    # case 1
    blocks.increase_difficulty(2)
    assert blocks.speed == (0.2 * 0.95)
    # no change may happen in this level range
    assert blocks.block_batch_max == 3
    # case 2
    blocks.reset()
    blocks.increase_difficulty(4)
    assert blocks.speed == (0.2 * 0.95)
    assert blocks.block_batch_max == 4
    # no change may happen in this level range
    assert blocks.block_batch_x_gap == 80
    # case 3
    blocks.reset()
    blocks.increase_difficulty(5)
    assert blocks.speed == (0.2 * 0.95)
    assert blocks.block_batch_max == 4
    assert blocks.block_batch_x_gap == (80 * 0.95)
    assert blocks.block_batch_y_gap == (25 * 0.95)
    # no change may happen in this level range
    assert blocks.block_batch_min == 0
    # case 4
    blocks.reset()
    blocks.increase_difficulty(77)
    assert blocks.speed == (0.2 * 0.95)
    assert blocks.block_batch_max == 4
    assert blocks.block_batch_x_gap == (80 * 0.95)
    assert blocks.block_batch_y_gap == (25 * 0.95)
    assert blocks.block_batch_min == 1



