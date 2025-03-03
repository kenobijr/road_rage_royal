from scoreboard import Scoreboard, Highscore
import os


def test_Scoreboard_init():
    """test correct default values on initialisation"""
    scoreboard = Scoreboard()
    assert scoreboard.level == 1
    assert scoreboard.font_type == "Courier"
    assert scoreboard.text_alignment == "left"
    assert not scoreboard._turtle.isdown()


def test_Scoreboard_increase_level():
    """test increasing the level"""
    scoreboard = Scoreboard()
    assert scoreboard.level == 1
    scoreboard.increase_level()
    assert scoreboard.level == 2


def test_Scoreboard_reset_level():
    """test reset the level after collision and player wants to play a further game"""
    scoreboard = Scoreboard()
    scoreboard.increase_level()
    scoreboard.reset_level()
    assert scoreboard.level == 1


def test_Highscore_init():
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
    highscore.highscore_db.remove_db_file()




