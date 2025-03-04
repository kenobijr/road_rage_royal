from src.highscore_db import HighscoreDB
import os
import pytest


@pytest.fixture
def clean_db():
    """
    - ensures that 'test_highscore.db' is removed before (and/or after) each test
    - resets the singleton so each test starts from scratch
    """
    # 1) Remove if exists
    db = HighscoreDB("data/test.highscore.db")
    db.reset_db()  # closes the connection, sets _instance=None, removes file
    yield


def test_HighscoreDB_init(clean_db):
    """test correct initialisation of the sqlite3 using alternative file path; before init file must not exist"""
    assert not os.path.isfile("data/test.highscore.db")
    db = HighscoreDB(db_path="data/test.highscore.db")
    assert os.path.isfile("data/test.highscore.db")


def test_HighscoreDB_get():
    """test retrieve the current highscore from the db"""
    db = HighscoreDB(db_path="data/test.highscore.db")
    assert db.get_highscore() == 1


@pytest.mark.parametrize(
    "initial_score, new_score, expected_score",
    [
        (1, 0, 1),
        (1, 1, 1),
        (1, 2, 2),
        (2, 10, 10)
    ]
)
def test_HighscoreDB_update_params(initial_score, new_score, expected_score):
    """test parameterized updating the highscore in the db; update only if new value higher than current value"""
    db = HighscoreDB(db_path="data/test.highscore.db")
    db.update_highscore(initial_score)
    assert db.get_highscore() == initial_score
    db.update_highscore(new_score)
    assert db.get_highscore() == expected_score


def test_HighscoreDB_remove_db_file():
    """test removing the local db file"""
    db = HighscoreDB(db_path="data/test.highscore.db")
    db.reset_db()
    assert not os.path.isfile("data/test.highscore.db")
