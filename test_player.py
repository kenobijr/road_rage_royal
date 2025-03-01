import pytest
from screen import GameScreen
from player import Player


def test_Player_init_attributes():
    """test the default values for player on initiating"""
    screen = GameScreen()
    player = Player(screen)
    assert player.start_x == 0
    assert player.start_y == -265
    assert player.width == 15
    assert player.height == 30
    assert player.move_distance == 10


def test_Player_init_attributes_screen():
    """test default values for player on initiating derived from the screen object delivered as param to Player"""
    screen = GameScreen()
    player = Player(screen)
    assert player.top_boundary == 250
    assert player.bottom_boundary == -240
    assert player.left_boundary == -298
    assert player.right_boundary == 296


def test_Player_init_player_turtle():
    """test initiation of the turtle object within Player"""
    screen = GameScreen()
    player = Player(screen)
    assert hasattr(player, "_turtle_player")
    assert player._turtle_player.shape() == "car.gif"
    assert not player._turtle_player.isdown()
    assert player._turtle_player.heading() == 90.0
    assert player._turtle_player.pos() == (0.0, -265.0)


def test_Player_valid_movements():
    """
    - test moving the player turtle in all supported directions for valid movements not crossing boundaries
    - start testing from pos (0.0, 0.0); move distance 10
    """
    screen = GameScreen()
    player = Player(screen)
    player._turtle_player.goto(0, 0)
    # test move up
    player.move_up()
    assert player._turtle_player.pos() == (0.0, 10.0)
    # test move right
    player.move_right()
    assert player._turtle_player.pos() == (10.0, 10.0)
    # test move down
    player.move_down()
    assert player._turtle_player.pos() == (10.0, 0.0)
    # test move left
    player.move_left()
    assert player._turtle_player.pos() == (0.0, 0.0)


def test_Player_invalid_movements():
    """
    - test moving the player turtle to cross boundaries, which is not allowed
    - start testing from default pos (0.0, -265); move distance 10
    - movements over top boundary not checked; this is prevented by teleporting player on crossing it
    """
    screen = GameScreen()
    player = Player(screen)
    # test move down from default start pos, which is not allowed
    player.move_down()
    assert player._turtle_player.pos() == (0.0, -265.0)
    # test move right must not change pos; right boundary equals 296
    player._turtle_player.goto(player.right_boundary, 0)
    player.move_right()
    assert player._turtle_player.pos() == (296.0, 0.0)
    # test move left must not change pos; left boundary equals -298
    player._turtle_player.goto(player.left_boundary, 0)
    player.move_left()
    assert player._turtle_player.pos() == (-298.0, 0.0)


def test_Player_reset_position():
    """test teleport method to bring player back to start position when reaching next level"""
    screen = GameScreen()
    player = Player(screen)
    # change player pos
    player._turtle_player.goto(0, 0)
    # execute reset & test it
    player.reset_position()
    assert player._turtle_player.pos() == (0.0, -265.0)


def test_Player_reset():
    """test teleport and reset player shape after collision and player opts for further round"""
    screen = GameScreen()
    player = Player(screen)
    # change player pos & shape
    player._turtle_player.goto(0, 0)
    player._turtle_player.shape("explosion.gif")
    # execute reset & test it
    player.reset()
    assert player._turtle_player.pos() == (0.0, -265.0)
    assert player._turtle_player.shape() == "car.gif"


def test_Player_getters():
    """test getters delivering data about player turtle state to outside callers"""
    screen = GameScreen()
    player = Player(screen)
    assert player.get_ycor() == player._turtle_player.ycor()
    assert player.get_xcor() == player._turtle_player.xcor()
    assert player.get_width() == player.width
    assert player.get_height() == player.height


def test_Player_update_shape():
    """test changing the player shape"""
    screen = GameScreen()
    player = Player(screen)
    player.update_shape("explosion.gif")
    assert player._turtle_player.shape() == "explosion.gif"
