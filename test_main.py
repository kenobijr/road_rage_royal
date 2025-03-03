from main import Game
from screen import GameScreen
from player import Player
from block_manager import BlockManager
from scoreboard import Scoreboard, Highscore
from unittest.mock import patch
import pytest


@patch("player.Turtle")
@patch("screen.Turtle")
@patch("screen.Screen")
@patch("scoreboard.Turtle")
@patch("block_manager.Turtle")
def test_Game_init(mock_block_turtle, mock_score_turtle, mock_screen_screen, mock_screen_turtle, mock_player_turtle):
    """test if game is initialised with correct attributes """
    new_game = Game()
    assert hasattr(new_game, "screen")
    assert isinstance(new_game.screen, GameScreen)
    assert hasattr(new_game, "player")
    assert isinstance(new_game.player, Player)
    assert hasattr(new_game, "blocks")
    assert isinstance(new_game.blocks, BlockManager)
    assert hasattr(new_game, "highscore")
    assert isinstance(new_game.highscore, Highscore)
    assert hasattr(new_game, "scoreboard")
    assert isinstance(new_game.scoreboard, Scoreboard)
    assert new_game.running


@patch("screen.Turtle")
@patch("scoreboard.Turtle")
@patch("block_manager.Turtle")
def test_Game_level_up(mock_block_turtle, mock_score_turtle, mock_screen_turtle):
    """test if level up form 1 to 2 function is working correctly; omit testing highscore"""
    new_game = Game()
    new_game._level_up()
    assert new_game.scoreboard.level == 2
    assert new_game.player._turtle_player.pos() == (0, -265)
    # level 1 to 2 increases only speed
    assert new_game.blocks.speed == 0.19


@pytest.mark.parametrize(
    "initial_x, initial_y, goal_reached",
    [
        (0, -265, False),
        (50, 0, False),
        (0, 260, False),
        (0, 261, True),
        (0, 280, True)
    ]
)
def test_Game_player_reached_goal(initial_x, initial_y, goal_reached):
    """parameterized test player reached goal (= upper boundary) to reach next level; returns true or false"""
    new_game = Game()
    new_game.player._turtle_player.goto(initial_x, initial_y)
    assert new_game._player_reached_goal() == goal_reached


@patch.object(GameScreen, "show_prompt", return_value="y")
def test_Game_ask_restart_yes(mock_prompt):
    """test restart function with mocked user prompt"""
    game = Game()
    assert game._ask_restart() is True


@patch.object(GameScreen, "show_prompt", return_value="n")
def test_Game_ask_restart_no(mock_prompt):
    """test restart function with mocked user prompt"""
    game = Game()
    assert game._ask_restart() is False






