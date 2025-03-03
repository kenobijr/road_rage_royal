from scoreboard import Scoreboard, Highscore
import pytest
from unittest.mock import patch


@pytest.fixture
def clean_highscore_db():
    """fixture to make sure test db is clean on every new testrun; used before initiating test db"""
    highscore = Highscore(file_path="test_highscore.db")
    highscore.db.reset_db()
    yield

def test_Scoreboard_init():
    """test correct default values on initialisation"""
    scoreboard = Scoreboard()
    assert scoreboard.level == 1
    assert scoreboard.font_type == "Courier"
    assert scoreboard.text_alignment == "left"
    assert not scoreboard._turtle.isdown()


@patch("scoreboard.Turtle")
def test_Scoreboard_increase_level(mock_turtle_class):
    """test increasing the level; patch out turtle since not needed"""
    scoreboard = Scoreboard()
    assert scoreboard.level == 1
    scoreboard.increase_level()
    assert scoreboard.level == 2


@patch("scoreboard.Turtle")
def test_Scoreboard_reset_level(mock_turtle_class):
    """test reset the level after collision & player wants to play a further game; patch out turtle since not needed"""
    scoreboard = Scoreboard()
    scoreboard.increase_level()
    scoreboard.reset_level()
    assert scoreboard.level == 1


def test_Highscore_init(clean_highscore_db):
    """test correct default values on initialisation"""
    highscore = Highscore(file_path="test_highscore.db")
    assert highscore.highscore == 1
    assert highscore.font_type == "Courier"
    assert highscore.text_alignment == "left"
    assert not highscore._turtle.isdown()


def test_Highscore_update():
    """test update highscore function when player reaches next level"""
    highscore = Highscore(file_path="test_highscore.db")
    # case 1: highscore may not be increased if level is lower than current highscore
    assert highscore.highscore == 1
    highscore.update_highscore(0)
    assert highscore.highscore == 1
    # case 2: update highscore for higher levels
    highscore.update_highscore(5)
    assert highscore.highscore == 5




