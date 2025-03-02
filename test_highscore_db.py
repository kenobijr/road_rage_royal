from highscore_db import HighscoreDB
import os


def test_HighscoreDB_init():
    """test correct initialisation of the sqlite3 using alternative file path; before init file must not exist"""
    assert not os.path.isfile("test_highscore.db")
    db = HighscoreDB(db_pass="test_highscore.db")
    assert os.path.isfile("test_highscore.db")


def test_HighscoreDB_get():
    """test retrieve the current highscore from the db"""
    db = HighscoreDB(db_pass="test_highscore.db")
    assert db.get_highscore() == 1


def test_HighscoreDB_update():
    """test updating the highscore in the db; update only if new value higher than current value"""
    db = HighscoreDB(db_pass="test_highscore.db")
    # case 1: no update for value 0, since lower than current value 1
    db.update_highscore(0)
    assert db.get_highscore() == 1
    # case 2: update for higher value 5
    db.update_highscore(5)
    assert db.get_highscore() == 5


def test_HighscoreDB_remove_db_file():
    """test removing the local db file"""
    db = HighscoreDB(db_pass="test_highscore.db")
    db.remove_db_file()
    assert not os.path.isfile("test_highscore.db")
