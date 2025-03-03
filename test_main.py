from main import Game
from screen import GameScreen
from player import Player
from block_manager import BlockManager
from scoreboard import Scoreboard, Highscore


def test_Game_init():
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


