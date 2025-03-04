from src.screen import GameScreen
from src.player import Player
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_turtle_and_screen():
    """
    - fixture to patch player.Turtle, screen.Screen and screen.Turtle
    - "\" in expression means “I’m continuing this statement on the next line”
    - works only for testcases NOT relying on positional / shape logic saved at Turtle objects
    - all these cases must use the real classes / objects to work out, even when triggering the GUI
    """
    with patch("src.player.Turtle") as mock_player_turtle_class, \
         patch("src.screen.Turtle") as mock_screen_turtle_class, \
         patch("src.screen.Screen") as mock_screen_screen_class:
        yield mock_player_turtle_class, mock_screen_turtle_class, mock_screen_screen_class


def test_Player_init_attributes(mock_turtle_and_screen):
    """test the default values for player on initiating; mocked without opening GUI"""
    screen = GameScreen()
    player = Player(screen)
    assert player.start_x == 0
    assert player.start_y == -265
    assert player.width == 15
    assert player.height == 30
    assert player.move_distance == 10


def test_Player_init_attributes_screen(mock_turtle_and_screen):
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
    assert player._turtle_player.shape() == "assets/car.gif"
    assert not player._turtle_player.isdown()
    assert player._turtle_player.heading() == 90.0
    assert player._turtle_player.pos() == (0.0, -265.0)


@pytest.mark.parametrize(
    "initial_x, initial_y, move_method, expected_x, expected_y",
    [
        (0, 0, "move_up", 0, 10),
        (0, 10, "move_right", 10, 10),
        (10, 10, "move_down", 10, 0),
        (10, 0, "move_left", 0, 0)
    ]
)
def test_Player_valid_movements_params(initial_x, initial_y, move_method, expected_x, expected_y):
    """
    single parametrized test that tries different movement scenarios:
    1. sets player's turtle to (initial_x, initial_y).
    2. calls the specified move_method (str).
    3. asserts we land at (expected_x, expected_y).
    """
    screen = GameScreen()
    player = Player(screen)
    # go to start pos
    player._turtle_player.goto(initial_x, initial_y)
    # get movement type and execute it
    getattr(player, move_method)()
    # check the current position after moving vs the expected pos
    assert player._turtle_player.pos() == (expected_x, expected_y)


@pytest.mark.parametrize(
    "initial_x, initial_y, move_method, expected_x, expected_y",
    [
        (0, -265, "move_down", 0, -265),
        (296, 0, "move_right", 296, 0),
        (-298, 0, "move_left", -298, 0),
    ]
)
def test_Player_invalid_movements_params(initial_x, initial_y, move_method, expected_x, expected_y):
    """
    - parametrized test moving the player turtle to cross boundaries, which is not allowed
    - movements over top boundary not checked; this is prevented by teleporting player on crossing it
    - same structure as for valid movements
    """
    screen = GameScreen()
    player = Player(screen)
    player._turtle_player.goto(initial_x, initial_y)
    getattr(player, move_method)()
    assert player._turtle_player.pos() == (expected_x, expected_y)


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
    player._turtle_player.shape("assets/explosion.gif")
    # execute reset & test it
    player.reset()
    assert player._turtle_player.pos() == (0.0, -265.0)
    assert player._turtle_player.shape() == "assets/car.gif"


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
    player.update_shape("assets/explosion.gif")
    assert player._turtle_player.shape() == "assets/explosion.gif"
